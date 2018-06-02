from app.core.database    import db
from app.app              import app
from app.core.converter   import Converter
from app.core.initializer import Initializer

with app.app_context():

    db.init_app(app)

    db.create_all()

    ini = Initializer()

    ini.init_metadata_database()


    # con = Converter()

    # print(convert(source_cur, destinion_cur, 1))
