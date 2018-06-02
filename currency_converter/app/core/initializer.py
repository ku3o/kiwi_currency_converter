import lxml.html

from os       import makedirs
from requests import get as r_get
from json     import dump as json_dump
from os.path  import exists as path_exists

from .database              import db, CurrencyMeta
from .constants.initializer import CURRENCY_DATA_URL


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

            abc_code     = columns[0].text.strip().upper()
            symbol       = columns[1].text.strip()
            digital_code = columns[2].text.strip()
            full_name    = columns[3].text.strip()
            county_name  = row.getchildren()[4].getchildren()[0].getchildren()[0].text.strip().

            if symbol is None or symbol == '':
                continue

            db.session.add(CurrencyMeta(abc_code     = abc_code,
                                        digital_code = digital_code,
                                        full_name    = full_name,
                                        contry_name  = contry_name,
                                        symbol       = symbol))
        db.session.commit()
