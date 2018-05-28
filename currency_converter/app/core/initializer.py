import lxml.html

from os       import makedirs
from requests import get as r_get
from json     import dump as json_dumps
from os.path  import exists as path_exists

from .constants.initializer import CURRENCY_DATA_URL
from .constants.paths       import CURRENCY_META_DATA_FILE, STORE_DIR, ABC_SYMBOL_META_FILE


class Initializer(object):
    def __init__(self):
        pass


    def init_metadata_database(self):
        # Download meta-data page and parse it
        page     = r_get(CURRENCY_DATA_URL)
        data     = lxml.html.fromstring(page.text)
        all_rows = data.xpath('//table/tbody/*')

        currencies    = {}
        convert_table = {}

        # <tr>
        #     <th class="ag-currencies_equal-col">Currency</th>
        #     <th class="ag-currencies_equal-col">Symbol</th>
        #     <th class="ag-currencies_equal-col">Digital code</th>
        #     <th>Name</th>
        #     <th>Country</th>
        # </tr>

        # <tr>
        #     <td>AED</td>
        #     <td>د.إ</td>
        #     <td>784</td>
        #     <td>UAE Dirham</td>
        #     <td>
        #         <ul>
        #             <li class="ag-flags-country_item icon-country-ae">UAE</li>
        #         </ul>
        #     </td>
        # </tr>


        for row in all_rows:
            columns = row.getchildren()

            abc_code = columns[0].text
            symbol   = columns[1].text

            if symbol is None or symbol == '':
                continue

            currencies[abc_code] = {
                'abc_code'    : abc_code,
                'symbol'      : symbol,
                'digital_code': columns[2].text,
                'name'        : columns[3].text,
                'state_code'  : row.getchildren()[4].getchildren()[0].getchildren()[0].text
            }

            if symbol not in convert_table:
                convert_table[symbol] = []

            convert_table[symbol].append(abc_code)

        if not path_exists(STORE_DIR):
            makedirs(STORE_DIR)

        with open(CURRENCY_META_DATA_FILE, 'w', encoding='utf-8') as filefp:
            json_dumps(currencies, filefp, indent = 4, sort_keys = True, ensure_ascii = False)

        with open(ABC_SYMBOL_META_FILE, 'w', encoding='utf-8') as filefp:
            json_dumps(convert_table, filefp, indent = 4, sort_keys = True, ensure_ascii = False)
