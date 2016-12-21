from db.helpers import *

def update_stats():
    print('test')
    tickers = get_ticker_list()
    for ticker in tickers:
        result = opentsdb_query([ticker], 'returns', '5y-ago')
        print(result)
