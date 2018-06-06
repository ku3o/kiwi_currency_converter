__author__ = 'Dmytro Safonov (dmytro.safonov@seznam.cz)'

from app.app import create_app


if __name__ == '__main__':
	create_app('../configs/development.py').run(debug = True, host='0.0.0.0')
