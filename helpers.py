import os, requests, json, time, datetime

opentsdb_url = "http://" \
        + os.environ.get("OPENTSDB_HOST") \
        + ":" + os.environ.get("OPENTSDB_PORT") \
        + "/api/"

def opentsdb_query():
    request_data = {
        "start": "5y-ago",
        "queries": [
            {
                "aggregator": "sum",
                "metric": "TSLA.price",
                "rate": "false",
                "tags": {
                    "company":"TSLA"
                }
            },
            {
                "aggregator": "sum",
                "metric": "ABC.price",
                "rate": "false",
                "tags": {
                    "company":"ABC"
                }
            }
        ]
    }
    request_url = opentsdb_url + "query?summary=true&details=true"
    response = requests.post(request_url, data = json.dumps(request_data))
    response_dict = response.json()
    return response_dict
