# from app.core.database    import db
from app.app              import app
from app.core.converter   import Converter
from app.core.initializer import Initializer
from sqlalchemy import and_


from app.core.database            import db, CurrencyMeta, CurrencyCache

with app.app_context():

    # db.init_app(app)

    # db.drop_all()
    # db.create_all()

    # ini = Initializer()

    # ini.init_metadata_database()

    # con = Converter()

    # print(con.convert('AED', 'BGN', 10))


    # db_results = db.session.query(CurrencyCache.convert_ratio, CurrencyCache.last_updated).filter(
    #                 and_(CurrencyCache.source_currency == 'GBP',
    #                      CurrencyCache.destination_currency == 'EUR')).get()

    db_results = db.session.query(CurrencyCache).get(('AEDz', 'BGN'))


    print(dir(db_results))

    print(db_results.convert_ratio)

    db_results.convert_ratio = 0.5

    print(db_results.convert_ratio)


    db.session.commit()