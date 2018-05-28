__author__ = 'Dmytro Safonov (dmytro.safonov@seznam.cz)'

from app.app import app
from flask   import jsonify

@app.route('/')
@app.route('/index')
def index():
    return jsonify({'message':"Hello, I'm currency converter app for Kiwi.com"})
