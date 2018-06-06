import pytest

from app.core.database import db as _db
from app.app           import create_app


@pytest.fixture(scope='session')
def app():
	app = create_app('../configs/testing.py')
	ctx = app.app_context()

	ctx.push()

	yield app

	ctx.pop()


@pytest.fixture(scope='session')
def db(app):
	_db.drop_all()
	_db.create_all()

	yield _db

	_db.drop_all()
