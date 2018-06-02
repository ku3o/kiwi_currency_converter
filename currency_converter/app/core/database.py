from time             import time
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class CurrencyMeta(db.Model):
    abc_code     = db.Column(type_       = db.String(3),
                             primary_key = True,
                             nullable    = False)
    
    digital_code = db.Column(type_    = db.Integer,
                             nullable = False)

    full_name    = db.Column(type_ = db.Text)

    contry_name  = db.Column(type_ = db.Text)

    symbol       = db.Column(type_    = db.String(3),
                             nullable = False)


class CurrencyCache(db.Model):
    source_currency      = db.Column(type_       = db.String(3),
                                     primary_key = True,
                                     nullable    = False)

    destination_currency = db.Column(type_       = db.String(3),
                                     primary_key = True,
                                     nullable    = False)

    convert_ratio        = db.Column(type_    = db.Float,
                                     nullable = False)

    last_updated         = db.Column(type_    = db.Integer,
                                     nullable = False,
                                     default  = time)
