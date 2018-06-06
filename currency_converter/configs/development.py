from app.core.constants.paths import DATABASE_FILE


SQLALCHEMY_DATABASE_URI = 'sqlite:///{0}'.format(DATABASE_FILE)

SQLALCHEMY_TRACK_MODIFICATIONS = False
