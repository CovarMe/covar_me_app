import os, requests, json, time, datetime

opentsdb_url = "http://" \
        + os.environ.get("OPENTSDB_HOST") \
        + ":" + os.environ.get("OPENTSDB_PORT") \
        + "/api/"

def opentsdb_query(companies, metrics):
    n = len(companies) * len(metrics)
    query_template = {
        "aggregator": "sum",
        "metric": "EWST.price",
        "rate": "false",
        "tags": {}
    }
    queries = [query_template] * n
    for i, met in enumerate(metrics):
        for j, com in enumerate(companies):
            queries[i + j]['metric'] = com + '.' + met
            queries[i + j]['rate'] = 'false'
            queries[i + j]['tags'] = {'company': com}

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
