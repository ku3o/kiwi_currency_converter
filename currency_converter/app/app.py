__author__ = 'Dmytro Safonov (dmytro.safonov@seznam.cz)'

from flask    import Flask
from os       import makedirs
from os.path  import exists as path_exists

app = Flask(__name__)

from app import views
from app.core.database import db
from app.core.constants.paths import DATABASE_FILE, DATABASE_DIR

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{0}'.format(DATABASE_FILE)

with app.app_context():
	if not path_exists(DATABASE_DIR):
		makedirs(DATABASE_DIR)

	db.init_app(app)
	# db.create_all()
