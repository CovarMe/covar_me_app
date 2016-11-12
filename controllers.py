from flask import render_template
from helpers import *

import random
names = ["Donald","Yoda","LeBron James", 
         "Theme", "Davide", "David", 
         "Jonas", "Santi", "World", 
         "Insect Overlords"]

def show_homepage():
    return render_template('index.html', 
                           name = random.choice(names))

def show_portfolio(username, portfolio_id):
    opentsdb_data = opentsdb_query()
    chart_data = []
    for metric in opentsdb_data:
        chart_data.append(metric['dps'])

    return render_template(
        'portfolio.html', 
        name = random.choice(names),
        chart_data = chart_data)

def show_registration_form():
    return render_template('registration.html')

def register_new_user():
    def login():
        if request.method == 'POST':
            do_the_login()
        else:
            show_the_login_form()
            return 404
