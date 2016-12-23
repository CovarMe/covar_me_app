# datamodels retrieve or transform the data for it to be in a desirable format
# for whatever needs to be displayed on a page

import numpy as np
import pandas as pd
from db.helpers import *
from calculations import *
from pprint import pprint


# returns the timeseries for the desired tickers in dataframe format
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


# calculates the optimal weights at different desired returns and puts return agains variance
def ret_vs_var_data_model(covar, returns):
    breaks = 100
    means = calculate_mean_vector(returns) * 100
    data = [(0,0)] * breaks
    for i in range(breaks):
        q = float(i) / breaks * 1000
        weights = calculate_wolf_weights(covar * 10000, means, q)
        var = np.absolute(np.dot(np.dot(weights.transpose(), covar * 10000), weights))
        data[i] = {'ret': q/100, 
                   'var': var/10000, 
                   'weights': weights,
                   'returns': means.tolist(),
                   'tickers': covar.index.tolist()}

    return data
