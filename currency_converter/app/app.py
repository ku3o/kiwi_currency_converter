__author__ = 'Dmytro Safonov (dmytro.safonov@seznam.cz)'

from flask    import Flask
from os       import makedirs
from os.path  import exists as path_exists

app = Flask(__name__)

from app.core.database        import db
from app                      import views
from app.core.constants.paths import DATABASE_DIR
from app.models               import CurrencyAPI
from app.core.initializer     import Initializer


def create_app(config=None):
    app = Flask(__name__)

    app.config.from_pyfile(config)

    if not path_exists(DATABASE_DIR):
        makedirs(DATABASE_DIR)

    db.init_app(app)

    with app.app_context():
        db.create_all()

        #
        # I know, it's a weired step. But I want have meta-data on the fly
        #
        Initializer().init_metadata_database()

    app.add_url_rule('/currency_converter',
                     view_func = CurrencyAPI.as_view('currency_converter'),
                     methods   = ['GET'])
    return app