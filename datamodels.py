import numpy as np
import pandas as pd
from db.helpers import *
from calculations import *
from pprint import pprint


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


def ret_vs_var_data_model(covar, returns):
    breaks = 20
    means = calculate_mean_vector(returns) * 100
    data = [(0,0)] * breaks
    for i in range(breaks):
        q = float(i) / breaks * 100
        weights = calculate_wolf_weights(covar, means, q)
        var = np.dot(np.dot(weights.transpose(), covar), weights)
        data[i] = {'ret': q, 
                   'var': var, 
                   'weights': weights,
                   'returns': means}

    return data
