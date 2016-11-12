# import all the required stuff
import os
from os.path import join, dirname
from dotenv import load_dotenv
from flask import Flask
from flask import render_template
from flask_bower import Bower
from mongoengine import connect

# set up the data models defined for mongo
from mongo_schemata import *

# load environment variables from .env file
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

import random
names = ["Donald","Yoda","LeBron James", 
         "Theme", "Davide", "David", 
         "Jonas", "Santi", "World", 
         "Insect Overlords"]

# create a Flask application
app = Flask(__name__)
# inject bower (for front-end resource management)
Bower(app)
# connect to MongoDB
connect(host='mongodb://' + os.environ.get('MONGO_HOST') + '/' + os.environ.get('MONGO_DBNAME'))

@app.route('/')
def home_page():
    return render_template('index.html',name = random.choice(names))

@app.route('/portfolio/<username>-<portfolio_id>')
def show_portfolio(username, portfolio_id):
    # show the given portfolio
    print 'User %s' % username
    return 'Portfolio %s' % portfolio_id
