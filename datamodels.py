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
    data = data.rename(index = str, columns = tickers)
    return data
