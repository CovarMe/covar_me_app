from flask import Flask
from flask_pymongo import PyMongo
from flask.views import View
from flask import render_template

app = Flask(__name__)
mongo = PyMongo(app)

@app.route('/')

def home_page():
    name = "james"
    return render_template('index.html',name=name)


