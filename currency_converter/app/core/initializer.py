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

            abc_code     = columns[0].text
            symbol       = columns[1].text
            digital_code = columns[2].text
            full_name    = columns[3].text
            contry_name  = ''

            if len(columns) >= 5:
                children_1 = columns[4].getchildren()
                if len(children_1) >= 1:
                    children_2 = children_1[0].getchildren()
                    if len(children_2) >= 0:
                        contry_name = children_2[0].text

            if symbol is None or symbol == '' or abc_code is None or abc_code == '':
                continue

            abc_code     = abc_code.strip().upper()
            symbol       = symbol.strip()
            digital_code = digital_code.strip() if digital_code is not None else ''
            full_name    = full_name.strip()    if full_name    is not None else ''
            contry_name  = contry_name.strip()  if contry_name  is not None else ''

            #
            # I know, it's a weired step. But I want have meta-data on the fly
            #
            if db.session.query(CurrencyMeta).get(abc_code) is None:
                db.session.add(CurrencyMeta(abc_code     = abc_code,
                                            digital_code = digital_code,
                                            full_name    = full_name,
                                            contry_name  = contry_name,
                                            symbol       = symbol))
        db.session.commit()
