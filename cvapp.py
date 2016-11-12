from flask import Flask
from flask_pymongo import PyMongo
from flask.views import View
from flask import render_template
import random
names = ["Donald","Yoda","LeBron James", 
         "Theme", "Davide", "David", 
         "Jonas", "Santi", "World", 
         "Insect Overlords"]

app = Flask(__name__)
mongo = PyMongo(app)

@app.route('/')

def home_page():
    return render_template('index.html',name = random.choice(names))

print(app)
