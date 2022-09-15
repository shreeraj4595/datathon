from fastapi import FastAPI
import json
import requests
import config

app = FastAPI()

@app.get("/first")
def hello(name = None):

    if name is None:
        text = 'Hello!'

    else:
        text = 'Hello ' + name + '!'

    return text

@app.get("/getPublishedDate")
def get_date_difference():
    url = config.endpoint_url

    payload = json.dumps({
    "version": True,
    "size": config.record_size,
    "sort": [
        {
        "_score": {
            "order": "desc"
        }
        }
    ],
    "query": {
        "bool": {
        "must": [],
        "filter": [
            {
            "match_all": {}
            },
            {
            "exists": {
                "field": "dates_accepted"
            }
            }
        ],
        "should": [],
        "must_not": []
        }
    },
    "_source": [
        "dates_accepted",
        "dates_online"
    ]
    })
    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)
    return json.loads(response.text)