__author__ = 'Dmytro Safonov (dmytro.safonov@seznam.cz)'

from app.app import app
# from app.core.database import db


if __name__ == '__main__':
	app.run(debug = True, host='0.0.0.0')
