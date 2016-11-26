import numpy as np
import pandas as pd
from db.helpers import *
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


from pydataset import data as std_data
# greedy algorithm to sort the matrix to look good on heatmap
def matrix_greedy_heatmap_sorted(tickers, matrix_name):
    mtcars = std_data('mtcars')
    data = pd.DataFrame(np.cov(mtcars),
                        index = mtcars.index,
                        columns = mtcars.index)
    # data = read_mongodb_matrix(tickers, 'precision')
    availbl = data.index.tolist()
    order = []
    for i in range(len(availbl) - 1):
        remain = data.loc[availbl, availbl]
        ldi = (remain[availbl[0]] - remain[availbl[1]]).idxmin()
        availbl.remove(ldi)
        order.append(ldi)

    return data.loc[order, order]
