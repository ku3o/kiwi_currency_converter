from time       import time
from sqlalchemy import and_
from datetime   import datetime
from requests   import get as r_get
from lxml.html  import fromstring as html_fromstr

from .database            import db, CurrencyCache
from .constants.converter import ONLINE_CONVERTER_URL, TIME_TO_LIFE


class Converter(object):

    def __init__(self, cache_timeout = TIME_TO_LIFE):
        self.cache_timeout    = cache_timeout
        self.error_template   = "Invalid '{0}' argument type. Expecting - '{1}', got - '{2}'"
        self.xpath_filter     = '//span[@class="uccResultAmount"]'
        self.requested_amount = 1


    def parse_page(self, text_html_data):
        data       = html_fromstr(text_html_data)
        ret_amount = data.xpath(self.xpath_filter)[0].text

        return float(ret_amount)


    def ask_online(self, source_cur, destinion_cur):
        if type(source_cur) is not str:
            raise ValueError(self.error_template.format(source_cur, str, type(source_cur)))

        if type(destinion_cur) is not str:
            raise ValueError(self.error_template.format(destinion_cur, str, type(destinion_cur)))

        if len(source_cur) != 3:
            raise ValueError("Invalid 'source_cur' argument format. Should be 3 letter string")

        if len(destinion_cur) != 3:
            raise ValueError("Invalid 'destinion_cur' argument format. Should be 3 letter string")

        source_cur    = source_cur.upper()
        destinion_cur = destinion_cur.upper()

        page = r_get(ONLINE_CONVERTER_URL,
                     params = {'Amount' : self.requested_amount,
                               'From'   : source_cur,
                               'To'     : destinion_cur})

        return self.parse_page(page.text)


    def convert(self, source_cur, destinion_cur, amount):
        if type(source_cur) is not str:
            raise ValueError(self.error_template.format(source_cur, str, type(source_cur)))

        if type(destinion_cur) is not str:
            raise ValueError(self.error_template.format(destinion_cur, str, type(destinion_cur)))

        if type(amount) in not int and type(amount) is not float:
            raise ValueError(self.error_template.format(amount, float, type(amount)))

        if len(source_cur) != 3:
            raise ValueError("Invalid 'source_cur' argument format. Should be 3 letter string")

        if len(destinion_cur) != 3:
            raise ValueError("Invalid 'destinion_cur' argument format. Should be 3 letter string")

        source_cur    = source_cur.upper()
        destinion_cur = destinion_cur.upper()

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
            else:
                convert_ratio = cached_entry.convert_ratio

        # Cache miss
        else:
            convert_ratio = self.ask_online(source_cur, destinion_cur)

            db.session.add(CurrencyCache(source_currency      = source_cur,
                                         destination_currency = destinion_cur,
                                         convert_ratio        = convert_ratio,
                                         last_updated         = current_ts))
            db.session.commit()

        return float(convert_ratio * requested_amount)
