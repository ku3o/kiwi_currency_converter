import pytest

from app.core.manager  import find_currency
from app.core.database import CurrencyMeta


tested_data = [
	({
		'abc_code'    : 'AZN',
		'digital_code': '944',
		'full_name'   : 'Azerbaijanian Manat',
		'contry_name' : 'Azerbaijan',
		'symbol'      : 'ман' 
	}, 'ман', 'AZN'),

	({
		'abc_code'    : 'BMD',
		'digital_code': '60',
		'full_name'   : 'Bermudian Dollar',
		'contry_name' : 'Bermuda',
		'symbol'      : '$' 
	}, '$', 'USD'),

	({
		'abc_code'    : 'AED',
		'digital_code': '784',
		'full_name'   : 'UAE Dirham',
		'contry_name' : 'UAE',
		'symbol'      : 'د.إ'
	}, 'د.إ', 'AED'),

	({
		'abc_code'    : 'CLP',
		'digital_code': '152',
		'full_name'   : 'Chilean Peso',
		'contry_name' : 'Chile',
		'symbol'      : '$' 
	}, '$' , 'USD'),

	({
		'abc_code'    : 'CUP',
		'digital_code': '192',
		'full_name'   : 'Cuban Peso',
		'contry_name' : 'Cuba',
		'symbol'      : '$' 
	}, 'CUP', 'CUP'),

	({
		'abc_code'    : 'USD',
		'digital_code': '840',
		'full_name'   : 'US Dollar',
		'contry_name' : 'American Samoa',
		'symbol'      : '$' 
	}, 'USD', 'USD'),

	({
		'abc_code'    : 'XXX',
		'digital_code': '111',
		'full_name'   : 'XXXXXXX',
		'contry_name' : 'XXXXX XXXXX',
		'symbol'      : '?' 
	}, 'YYY', None)
]


@pytest.fixture(scope='module')
def fill_up_db(db):
    for d in tested_data:
        db.session.add(CurrencyMeta(**d[0]))

    db.session.commit()


@pytest.mark.parametrize("obj,in_currency,out_currency", tested_data)
def test_find_currency(fill_up_db, obj, in_currency, out_currency):
    assert find_currency(in_currency) == out_currency
