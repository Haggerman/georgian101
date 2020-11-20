import flask
from flask import request

#aaa
georgianApp = flask.Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    year = request.args['year']
    try:
        return year
    except KeyError:
        return 'Invalid input'

