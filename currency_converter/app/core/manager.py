from .converter         import Converter
from .constants.manager import WTF_SYMBOLS
from .database          import db, CurrencyMeta


def find_currency(currency):
    currency = WTF_SYMBOLS.get(currency, currency)

    # Try to find by primary key => 3-letter code
    db_entry  = db.session.query(CurrencyMeta).get(currency.upper())

    # Hit by primary key
    if db_entry is not None:
        return db_entry.abc_code

    # Try to find by symbol
    db_entry  = db.session.query(CurrencyMeta.abc_code).filter(CurrencyMeta.symbol == currency).first()

    if db_entry is not None:
        return db_entry[0]

    return None


def convert(source_cur, destination_cur, amount):
    converter     = Converter()
    ret_structure = {
        'input' : {
            'amount'   : 0.0,
            'currency' : ''
        },
        'output' : {}
    }

    if type(source_cur) is not str:
        raise ValueError("Invalid 'source_cur' argument type. Expecting - 'str', got - '{2}'".format(type(source_cur)))

    try:
        amount = float(amount)
    except ValueError as e:
        raise ValueError("Unable cast 'amount' value to float")

    src_cur = find_currency(source_cur)

    if src_cur is None:
        raise ValueError('Unkonw source currency')

    ret_structure['input']['amount']   = amount
    ret_structure['input']['currency'] = src_cur

    if destination_cur is not None:
        dst_cur = find_currency(destination_cur)

        if dst_cur is None:
            raise ValueError('Unkonw destination currency')

        ret_structure['output'][dst_cur] = converter.convert(src_cur,
                                                             dst_cur,
                                                             amount)
    else:
        for dst_cur in db.session.query(CurrencyMeta.abc_code).all():
            ret_structure['output'][dst_cur[0]] = converter.convert(src_cur,
                                                                    dst_cur[0],
                                                                    amount)
    return ret_structure
