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
    data = {}
    opentsdb_res = opentsdb_query(
        ['EGAS'],
        ['price']
    )
    if opentsdb_res['success']:
        data['ts'] = []
        for metric in opentsdb_res['data']:
            data['ts'].append(metric['dps'])

    data['ret_vs_var'] = [{
          'x': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 
          'y': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 
          'line': {'color': "rgb(0,100,80)"}, 
          'mode': "lines", 
          'name': "Fair", 
          'type': "scatter"
    }]

    return render_template(
        'portfolio.html', 
        name = random.choice(names),
        data = data)


def show_new_portfolio_form(username):
    tickers = get_ticker_list()
    return render_template('new_portfolio.html',
                           username = username,
                           tickers = tickers)


def create_new_portfolio(form):
    return form


def show_registration_form():
    return render_template('registration.html')


def register_new_user():
    def login():
        if request.method == 'POST':
            do_the_login()
        else:
            show_the_login_form()
            return 404
