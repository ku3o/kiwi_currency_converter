from time       import time
from sqlalchemy import and_
from datetime   import datetime
from requests   import get as r_get
from lxml.html  import fromstring as html_fromstr

from .database            import db, CurrencyMeta, CurrencyCache
from .constants.converter import ONLINE_CONVERTER_URL, TIME_TO_LIFE


class Converter(object):

    def __init__(self, cache_timeout = TIME_TO_LIFE):
        self.cache_timeout = cache_timeout


    def ask_online(self, source_cur, destinion_cur):
        page = r_get(ONLINE_CONVERTER_URL,
                     params = {'Amount' : 1,
                               'From'   : source_cur,
                               'To'     : destinion_cur})

        data = html_fromstr(page.text)

        ret_amount = data.xpath('//span[@class="uccResultAmount"]')[0].text

        return float(ret_amount)


    def convert(self, source_cur, destinion_cur, amount):
        error_template = "Invalid '{0}' argument type. Expecting - '{1}', got - '{2}'"

        if type(source_cur) is not str:
            raise ValueError(error_template.format(source_cur, str, type(source_cur)))

        if type(destinion_cur) is not str:
            raise ValueError(error_template.format(destinion_cur, str, type(destinion_cur)))

        requested_amount = 0.0

        try:
            requested_amount = float(amount)
        except ValueError as e:
            raise ValueError("Invalid 'amount' argument data. Can't cast to FLOAT")

        current_ts    = int(time())
        convert_ratio = None
        cached_entry  = db.session.query(CurrencyCache).get((source_cur, destinion_cur))

        # Cache hit
        if cached_entry is not None:

            # Check cache timeout
            if current_ts - cached_entry.last_updated >= self.cache_timeout:
                convert_ratio = self.ask_online(source_cur, destinion_cur)

                cached_entry.convert_ratio = convert_ratio

                db.session.commit()

        # Cache miss
        else:
            convert_ratio = self.ask_online(source_cur, destinion_cur)

            db.session.add(CurrencyCache(source_currency      = source_cur,
                                         destination_currency = destinion_cur,
                                         convert_ratio        = convert_ratio,
                                         last_updated         = current_ts))
            db.session.commit()

        return float(convert_ratio * requested_amount)
