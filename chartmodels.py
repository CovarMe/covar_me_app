# this prepares all the chart data in the format required for the
# front-end javascript charting libraries

import math
import random
import datetime
from db.helpers import *
from db.mongo_schemata import *

def ret_vs_var_chart_model(ret_vs_var):
    data = [{
        'y': ["%.2f" % float(e['ret']) for e in ret_vs_var], 
        'x': ["%.2f" % float(e['var']) for e in ret_vs_var], 
        'line': {'color': "rgb(0,100,80)"}, 
        'mode': "lines", 
        'name': "Ret vs. Risk", 
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


def portfolio_network_chart_model(covar, standardise = True):
    if standardise == True:
        covar = (covar - np.mean(covar, axis = 0)) \
                / np.std(covar, axis=0)

    data = {'nodes':[], 'edges':[]}
    data['nodes'] = map(lambda x: {'id':x,'label':x}, set(covar.index.tolist()))
    it = np.nditer(covar, flags=['f_index','multi_index'])
    while not it.finished:
        if it.multi_index[0] < it.multi_index[1] and abs(it[0]) > 0.5:
            edge = {
                'from': covar.index.tolist()[it.multi_index[0]],
                'to': covar.index.tolist()[it.multi_index[1]],
                'value': "%.2f" % float(abs(it[0])),
                'color': '#cad49d' if it[0] > 0 else '#c89fa3'
            }
            data['edges'].append(edge)

        it.iternext()

    if len(data['edges']) > 50:
      data['edges'] = [e for e in data['edges'] if e['color'] == '#cad49d']

    return data
