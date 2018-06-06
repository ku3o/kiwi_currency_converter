import pytest

from time import time

from app.core.converter import Converter
from app.core.database  import CurrencyMeta, CurrencyCache

tested_data = [
    ({
        'source_currency': 'AAA',
        'destination_currency': 'BBB',
        'convert_ratio': 0.1
    }, 10, 1),

    ({
        'source_currency': 'CCC',
        'destination_currency': 'DDD',
        'convert_ratio': 0.2
    }, 10, 2),

    ({
        'source_currency': 'EEE',
        'destination_currency': 'FFF',
        'convert_ratio': 0.3
    }, 10, 3)
]


@pytest.fixture(scope='module')
def fill_up_db(db):
    for d in tested_data:
        db.session.add(CurrencyCache(**d[0]))

    db.session.commit()


@pytest.fixture(scope='module')
def converter():
    yield Converter()


# convert - Invalid first argument

# convert - Invalud second argumet

# convert - Invalud third argument

# convert - Cache miss (check db after call)

# convert - Cache hit and timeout (check db after call)

# convert - Cache hit - convert without call
@pytest.mark.parametrize("obj,in_amount,out_amount", tested_data)
def test_cache_hit(fill_up_db, converter, obj, in_amount, out_amount):
    test_amount = converter.convert(source_cur    = obj['source_currency'],
                                    destinion_cur = obj['destination_currency'],
                                    amount        = in_amount)

    assert test_amount == out_amount


# ask_online - Invalid first argument

# ask_online - Invalud second argumet

# ask_online - Fallback after call