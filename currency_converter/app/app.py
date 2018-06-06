__author__ = 'Dmytro Safonov (dmytro.safonov@seznam.cz)'

from flask    import Flask
from os       import makedirs
from os.path  import exists as path_exists

app = Flask(__name__)

from app.core.database        import db
from app                      import views
from app.core.constants.paths import DATABASE_DIR



def create_app(config=None):
    app = Flask(__name__)

    app.config.from_pyfile(config)

    if not path_exists(DATABASE_DIR):
        makedirs(DATABASE_DIR)

    db.init_app(app)
    # db.create_all()

    return app