import timeit
import math
from flask import render_template, flash
from db.helpers import *

import random
names = ["Donald","Yoda","LeBron James", 
         "Theme", "Davide", "David", 
         "Jonas", "Santi", "World", 
         "Insect Overlords"]


def show_homepage():
    return render_template('index.html', 
                           name = random.choice(names))


def show_registration_form():
    return render_template('registration.html')

def register_new_user(form):
    errors = []
    if check_user(form['name']):
        errors.append('Username already exists, choose another name or log in.')

    if form['password1'] != form['password2']:
        errors.append("Passwords don't match.")

    try:
        u = create_user(name = form['name'],
                        email = form['email'],
                        password = form['password1'])
    except NotUniqueError:
        errors.append('Already taken!')

    if len(errors) > 0:
        for error in errors:
            flash(error, 'error')

        return show_registration_form()
    else:
        flash('New user ' + u.name + ' created!')
        return show_new_portfolio_form(u.name)


def show_login_form():
    return render_template('login.html')


def login_user(form):
    errors = []
    print(form)
    u = auth_user(form['email'], form['password'])
    if not u:
        errors.append("Can't log in with those credentials")

    if len(errors) > 0:
        for error in errors:
            flash(error, 'error')

        return show_login_form()
    else:
        return show_portfolio_list(u.name)


def show_portfolio_list(username):
    u = User.objects(name = username).first()
    return render_template('portfolio_list.html',
                           name = u.name,
                           portfolios = u.portfolios)


def show_new_portfolio_form(username):
    tickers = get_ticker_list()
    return render_template('new_portfolio.html',
                           username = username,
                           tickers = tickers)


def create_new_portfolio(username, name, tickers):
    portfolio_id = create_portfolio(username = username,
                                    name = name,
                                    tickers = tickers)
    return show_portfolio(username, portfolio_id) 


# TODO
def show_portfolio(username, portfolio_id):
    p = get_portfolio(portfolio_id)
    data = {}
    opentsdb_res = opentsdb_query(
        [s['ticker'] for s in p.stocks],
        ['price']
    )
    if opentsdb_res['success']:
        data['ts'] = []
        for metric in opentsdb_res['data']:
            data['ts'].append(metric['dps'])

    data['ret_vs_var'] = [{
        'x': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 
        'y': [math.log(i) for i in range(1,11)], 
        'line': {'color': "rgb(0,100,80)"}, 
        'mode': "lines", 
        'name': "Fair", 
        'type': "scatter"
    }]

    return render_template(
        'portfolio.html', 
        name = random.choice(names),
        data = data)


# TODO
def matrix_test():
    # mat = np.eye(100, dtype = float)
    start = time.clock()
    # create_mongodb_covar_matrix(mat, range(100))
    mat = read_mongodb_covar_matrix(range(25,45))
    end = time.clock()
    # return str(end - start)
    return mat 
