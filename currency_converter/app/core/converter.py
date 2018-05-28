import lxml.html

from os       import makedirs
from time     import time
from requests import get as r_get
from json     import dump as json_dump, load as json_load
from os.path  import exists as path_exists

from .constants.convert import ONLINE_CONVERTER_URL
from .constants.paths   import (CURRENCY_META_DATA_FILE, 
                                ABC_SYMBOL_META_FILE,
                                CURRENCY_CACHE_DIR,
                                CURRENCY_CACHE_FILE)


def load_json_file(file_name):
    if path_exists(file_name):
        with open(file_name, 'r') as filefp:
            return json_load(filefp)

    return {}


class Converter(object):

    def __init__(self, cache_timeout = 900):
        pass


    def laod_meta_data(self):
        self.abc_symbol_table = load_json_file(ABC_SYMBOL_META_FILE)
        self.currency_table   = load_json_file(CURRENCY_META_DATA_FILE)


    def update_cache(self, source_cur, destinion_cur, value):
        if source_cur not in self.cache_db:
            self.cache_db[source_cur] = {}

        self.cache_db[source_cur][destinion_cur] = value

        #
        # ADD THREADING SAFE !!!!!!!
        #
        self.store_cache_db()


    def load_cache_db(self):
        self.cache_db = load_json_file(CURRENCY_CACHE_FILE)


    def store_cache_db(self):
        if not path_exists(CURRENCY_CACHE_DIR):
            makedirs(CURRENCY_CACHE_DIR)

        with open(CURRENCY_CACHE_FILE, 'w') as filefp:
            json_dump(self.cache_db, filefp, indent = 4, sort_keys = True)


    def ask_online(self, source_cur, destinion_cur):
        page = r_get(ONLINE_CONVERTER_URL,
                     params = {'Amount' : 1, 'From' : source_cur, 'To' : destinion_cur})

        data = lxml.html.fromstring(page.text)

        ret_amount = data.xpath('//span[@class="uccResultAmount"]')[0].text

        return float(ret_amount)


    def convert(self, source_cur, destinion_cur, amount):
        # Cache hit

            # Cache hit, but cache timeout applied


        # Otherwise grab data from online service

            # Update cached value

        return (ret_amount, float(amount) * float(ret_amount) , time())