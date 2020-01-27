#http://flask.pocoo.org/docs/1.0/quickstart/#a-minimal-application
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'Index Page'

@app.route('/hello')
def hello():
    return '<b>Hello, World</b>'

