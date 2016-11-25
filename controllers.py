import timeit
import string
from flask import render_template, flash
from db.helpers import *
from chartmodels import *
from datamodels import *

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


def show_portfolio(username, portfolio_id):
    portfolio = get_portfolio(portfolio_id)
    tickers = [s['ticker'] for s in portfolio.stocks]
    # retrieve the corresponding returns timelines as a dataframe
    returns = returns_as_dataframe(tickers, '5y-ago')
    covar = read_mongodb_covar_matrix(list(string.ascii_lowercase[0:15]))
    # create chart data elements for all the different js charts 
    chart_data = {}
    chart_data['covar_heatmap'] = covar_heatmap_chart_model(covar)
    chart_data['ret_vs_var'] = ret_vs_var_chart_model(tickers)
    chart_data['noise'] = noise_chart_model(returns)
    return render_template(
        'portfolio.html', 
        name = random.choice(names),
        data = {
            'charts': chart_data
        })


# TODO
def matrix_test():
    start = time.clock()
    new_mat = np.random.rand(15,15)
    create_mongodb_covar_matrix(new_mat, list(string.ascii_lowercase[0:15]))
    mat = read_mongodb_covar_matrix(range(15,45))
    end = time.clock()
    return str(end - start)
