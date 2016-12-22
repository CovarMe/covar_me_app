import timeit
import string
from flask import render_template, flash
from db.helpers import *
from chartmodels import *
from datamodels import *


if os.environ.get('PRESENTATION') != None:
    with open(os.environ.get('PRESENTATION')) as f:
        rmdhtml = f.read().decode('utf-8')

def show_homepage():
    return render_template('index.html')

def show_about():
    return render_template('about.html')

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
    means = calculate_mean_vector(returns)
    # retrieve the corresponsing covariances
    covar = read_mongodb_matrix(tickers, 'covariance')
    resid_correl = calculate_residual_correlation_matrix(returns.fillna(0))
    # calculate return vs variance
    ret_vs_var = ret_vs_var_data_model(covar, returns)
    # sort the covariance for the heatmap
    resid_correl_sorted = matrix_greedy_heatmap_sorted(resid_correl)
    # create chart data elements for all the different js charts 
    chart_data = {}
    chart_data['covar_heatmap'] = covar_heatmap_chart_model(resid_correl_sorted)
    chart_data['ret_vs_var'] = ret_vs_var_chart_model(ret_vs_var)
    chart_data['noise'] = noise_chart_model(returns)
    chart_data['network'] = portfolio_network_chart_model(shrink_matrix(resid_correl))
    return render_template(
        'portfolio.html', 
        username = username,
        name = portfolio.name,
        tickers = tickers,
        data = {
            'charts': chart_data,
            'table': zip(tickers, np.round(means,3))
        })


def show_database_stats():
    tickers_available = len(get_ticker_list())
    tickers_total = len(get_ticker_list(filtered = False))
    matrix_items_stored = get_matrix_size('covariance')
    return render_template('database.html',
                           tickers_available = tickers_available,
                           tickers_total = tickers_total,
                           matrix_items_stored = matrix_items_stored)


# TODO
def matrix_test():
    start = time.clock()
    mtcars = std_data('mtcars')
    create_mongodb_matrix(np.cov(mtcars), mtcars.index.tolist(), 'covariance')
    mat = read_mongodb_matrix(mtcars.index.tolist(), 'covariance')
    end = time.clock()
    return str(end - start)
