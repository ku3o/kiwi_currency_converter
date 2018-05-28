__author__ = 'Dmytro Safonov (dmytro.safonov@seznam.cz)'

from flask import Flask

app = Flask(__name__)

from app import views
