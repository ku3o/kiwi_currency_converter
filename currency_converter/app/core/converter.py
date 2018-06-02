import lxml.html

from time       import time
from sqlalchemy import and_
from datetime   import datetime
from requests   import get as r_get

from .database            import db, CurrencyMeta, CurrencyCache
from .constants.converter import ONLINE_CONVERTER_URL, TIME_TO_LIFE


class Converter(object):

    def __init__(self, cache_timeout = TIME_TO_LIFE):
        self.cache_timeout = cache_timeout


    def ask_online(self, source_cur, destinion_cur):
        page = r_get(ONLINE_CONVERTER_URL,
                     params = {'Amount' : 1, 'From' : source_cur, 'To' : destinion_cur})

        data = lxml.html.fromstring(page.text)

        ret_amount = data.xpath('//span[@class="uccResultAmount"]')[0].text

        return float(ret_amount)


    def convert(self, source_cur, destinion_cur, amount):
        #
        # ADD TYPE CHECK
        #

        # Check cache hit
        current_ts    = int(time())
        convert_ratio = None
        last_updated  = None

        db_results = db.session.query(CurrencyCache.convert_ratio, CurrencyCache.last_updated).filter(
                        and_(CurrencyCache.source_currency == source_cur,
                             CurrencyCache.destination_currency == destinion_cur)).first()

        # Cache hit
        if db_results is not None:
            convert_ratio = db_results[0]
            last_updated  = db_results[1]

            # Check cache timeout
            if current_ts - last_updated < self.cache_timeout:
                convert_ratio = self.ask_online(source_cur, destinion_cur)

                # Update convert ratio
                new_rest = db.session.query(CurrencyCache.convert_ratio, CurrencyCache.last_updated).filter(
                            and_(CurrencyCache.source_currency == source_cur,
                                 CurrencyCache.destination_currency == destinion_cur)).update(
                                  {CurrencyCache.convert_ratio : convert_ratio,
                                   CurrencyCache.last_updated: current_ts}, synchronize_session='fetch')

                db.session.commit()

        # Cache miss
        else:
            convert_ratio = self.ask_online(source_cur, destinion_cur)
    
            new_entry = CurrencyCache(source_currency      = source_cur,
                                      destination_currency = destinion_cur,
                                      convert_ratio        = convert_ratio,
                                      last_updated         = current_ts)

            db.session.add(new_entry)
            db.session.commit()

        return convert_ratio * amount