from fastapi import FastAPI
import json
import requests
import config
import db
import uvicorn
import json
import logging
from logging.handlers import RotatingFileHandler

app = FastAPI()

logging.basicConfig(
    handlers=[RotatingFileHandler("app.log", maxBytes=100000, backupCount=10)],
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
)


@app.get("/getPublishedDate")
def get_date_difference():
    url = config.endpoint_url

    payload = json.dumps(
        {
            "version": True,
            "size": config.record_size,
            "sort": [{"_score": {"order": "desc"}}],
            "query": {
                "bool": {
                    "must": [],
                    "filter": [
                        {"match_all": {}},
                        {"exists": {"field": "dates_accepted"}},
                    ],
                    "should": [],
                    "must_not": [],
                }
            },
            "_source": ["dates_accepted", "dates_online"],
        }
    )
    headers = {"Content-Type": "application/json"}

    response = requests.request("GET", url, headers=headers, data=payload)

    logging.info(response.text)
    return json.loads(response.text)


@app.get("/getSubjectAreaData")
def get_subject_data(limit: int = 100, sub_area: str = "", skip: int = 0):
    """
    This API is used to query the set of data from Artifacts table.
    limit is default to 100, can be passed other values from the caller
    sub area can be queried for particular value not mandatory
    skip is the offset to specify from what record to query for default to 0
    """
    ret = db.get_subject_data(limit, skip, sub_area)
    if ret == "":
        return {"code": 500, "message": "Oops! Something went wrong"}
    # logging.info(ret)
    return ret


@app.get("/getSubjectArea")
def get_subject_list(limit: int = 100, skip: int = 0):
    """
    This API is used to get the list of subject area. This DB query takes lot of time, use with caution and only if necessary
    limit is default to 100, can be passed other values from the caller
    skip is the offset to specify from what record to query for default to 0
    """
    ret = db.get_subject_data_list(limit, skip)
    if ret == "":
        return {"code": 500, "message": "Oops! Something went wrong"}
    # logging.info(ret)
    return ret


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8082)
