import numpy as np
import pandas as pd
from db.helpers import *
from pprint import pprint
from pydataset import data as std_data


def returns_as_dataframe(tickers, since = '1y-ago'):
    db_res = opentsdb_query(tickers,
                            ['return'],
                            since)
    if db_res['success']:
        ts = []
        tickers = {}
        for i, metric in enumerate(db_res['data']):
            ts.append(metric['dps'])
            tickers[i] = metric['tags']['company']

    else:
        raise RuntimeError(db_res['error'])

    data = pd.DataFrame.from_dict(ts).transpose()
    data = data.rename(index = str, columns = tickers) # add the tickers as column names
    data = data.multiply(100) # make percentage-wise values
    return data


# greedy algorithm to sort the matrix to look good on heatmap
def matrix_greedy_heatmap_sorted(data):
    availbl = data.index.tolist()
    order = []
    for i in range(len(availbl) - 1):
        remain = data.loc[availbl, availbl]
        ldi = (remain[availbl[0]] - remain[availbl[1]]).idxmin()
        availbl.remove(ldi)
        order.append(ldi)

    return data.loc[order, order]


def calculate_mean_vector(returns):
    n = len(list(returns))
    data = [0] * n
    for i, ticker in enumerate(list(returns)):
        data[i] = returns[ticker].mean()

    return np.array(data)


def calculate_wolf_weights(covar, means, q):
    # Ledoit, Olivier, and Michael Wolf. 
    # "Improved estimation of the covariance matrix of stock returns with an application to portfolio selection." 
    # Journal of empirical finance 10.5 (2003): 603-621
    n = len(list(covar)) # number of companies
    sigma = covar.as_matrix() # covariance matrix
    prec = np.linalg.inv(sigma) # precision matrix
    ones = np.ones(n)
    A = np.dot(np.dot(ones.transpose(), prec), ones)
    B = np.dot(np.dot(ones.transpose(), prec), means)
    C = np.dot(np.dot(means.transpose(), prec), means)
    denom = (A * C - B ** 2)
    w = np.dot(np.dot((C - q * B) / denom, prec),ones) + \
            np.dot(np.dot((q * A - B) / denom, prec), means)
    print(q)
    return w
