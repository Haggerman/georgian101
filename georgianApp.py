import flask
from flask import request

georgianApp = flask.Flask(__name__)

@georgianApp.route('/', methods=['GET'])
def home():
    year = request.args['year']
    try:
        return year
    except KeyError:
        return 'Invalid input'

