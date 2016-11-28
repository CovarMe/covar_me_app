import math
import random
import datetime
from db.helpers import *
from db.mongo_schemata import *

def ret_vs_var_chart_model(tickers):
    var = [math.log(i) for i in range(1,11)]
    ret = range(1,10)
    data = [{
        'x': ret, 
        'y': var, 
        'line': {'color': "rgb(0,100,80)"}, 
        'mode': "lines", 
        'name': "Fair", 
        'type': "scatter"
    }]
    return data


def noise_chart_model(returns):
    data = []
    dates = map(lambda d:
                datetime.datetime.fromtimestamp(
                    int(d)
                ).strftime('%Y/%m/%d'),
                returns.index)
    for i, ticker in enumerate(returns):
        data.append({
            'x': dates, 
            'y': returns[ticker].tolist(), 
            'line': {
              'color': "rgb(" + ",".join(str(random.sample(range(0, 255), 3))) + ")",
              'width': 0.5
            }, 
            'mode': "lines", 
            'name': ticker, 
            'type': "scatter"})

    return data


def covar_heatmap_chart_model(covar):
    data = [{
        'type': 'heatmap',
        'x': covar.index.tolist(),
        'y': list(covar),
        'z': covar.as_matrix().tolist()
    }]
    return data


def portfolio_network_chart_model(covar):
    data = {'nodes':[], 'edges':[]}
    data['nodes'] = map(lambda x: {'id':x,'label':x}, set(covar.index.tolist()))
    it = np.nditer(covar, flags=['f_index','multi_index'])
    while not it.finished:
        if it.multi_index[0] < it.multi_index[1] and it[0] > 2:
            edge = {
                'from': covar.index.tolist()[it.multi_index[0]],
                'to': covar.index.tolist()[it.multi_index[1]],
                'value': "%.2f" % float(it[0])
            }
            print edge
            data['edges'].append(edge)

        it.iternext()

    return data
