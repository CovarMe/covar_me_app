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
