import threading
from db.helpers import *


def background_update_stats():
    thread = threading.Thread(target = update_stats)
    thread.start()


def update_stats():
    tickers = get_ticker_list(filtered = False)
    for ticker in tickers:
        status = {}
        db_res = opentsdb_query([ticker], ['return'], '5y-ago')
        if db_res['success']:
            metric = db_res['data'][0]
            ts = metric['dps']
            res_ticker = metric['tags']['company']
            if ticker == res_ticker:
                status['ts'] = 'available'

        elif db_res['error'] == 'Missing queries' \
                or db_res['error'] == 'Empty response.':
            status['ts'] = 'missing'

        else:
            raise RuntimeError(db_res['error'])

        cov = read_mongodb_matrix([ticker], 'covariance')
        if type(cov) == pd.DataFrame:
            status['cov'] = 'available'

        else:
            status['cov'] = 'missing'

        update_stock_status(ticker, status)
        print(ticker)
        print(status)
