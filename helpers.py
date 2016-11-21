import os, requests, json, time, datetime
import numpy as np
from mongo_schemata import *

opentsdb_url = "http://" \
        + os.environ.get("OPENTSDB_HOST") \
        + ":" + os.environ.get("OPENTSDB_PORT") \
        + "/api/"


def get_ticker_list(q = ''):
    tickers = [stock['ticker'] for stock in Stock.objects(ticker__contains = q)]
    return sorted(tickers)


def opentsdb_query(companies, metrics):
    n = len(companies) * len(metrics)
    query_template = {
        "aggregator": "sum",
        "rate": "false",
        "tags": {}
    }
    queries = [query_template] * n
    for i, met in enumerate(metrics):
        for j, com in enumerate(companies):
            queries[i + j]['metric'] = com + '.' + met
            queries[i + j]['rate'] = 'false'
            queries[i + j]['tags'] = { 'company': com }

    request_data = {
        "start": "5y-ago",
        "queries": queries
    }
    request_url = opentsdb_url + "query?summary=true&details=true"
    response = requests.post(request_url, data = json.dumps(request_data))
    response_dict = response.json()
    if 'error' in response_dict:
        return {'success': False, 'error': response_dict['error']['message']}
    elif len(response_dict) == 0:
        return {'success': False, 'error': 'Empty response.'}
    else:
        return {'success': True, 'data': response_dict}


def create_mongodb_covar_matrix(mat, names):
    it = np.nditer(mat, flags=['f_index','multi_index'])
    while not it.finished:
        if it.multi_index[0] <= it.multi_index[1]:
            print('Create covariance cell: ' + str(it[0]))
            MatrixItem.objects(i = names[it.multi_index[0]],
                               j = names[it.multi_index[1]]
                              ).update_one(set__v = it[0], upsert = True)

        it.iternext()

    return " ".join([(str(mi['i']) + str(mi['j']) + ": " + str(mi['v'])) for mi in MatrixItem.objects()])


def read_mongodb_covar_matrix(names):
    mis = MatrixItem.objects(i__in = names,
                             j__in = names)
    print(mis)
    return " ".join([(str(mi['i']) + str(mi['j']) + ": " + str(mi['v'])) for mi in mis])

