import logging
from logging.handlers import RotatingFileHandler
import json
import requests
import config

logging.basicConfig(
    handlers=[RotatingFileHandler("app.log", maxBytes=100000, backupCount=10)],
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
)


def get_dates_diff():
    url = config.endpoint_url

    payload = json.dumps(
        {
            "version": True,
            "size": config.record_size,
            "sort": [{"_score": {"order": "asc"}}],
            "query": {
                "bool": {
                    "must": [],
                    "filter": [
                        {"match_all": {}},
                        {"exists": {"field": "subject_areas_crossref_0"}},
                    ],
                    "should": [],
                    "must_not": [],
                }
            },
            "_source": ["subject_areas_crossref_0"],
        }
    )
    headers = {"Content-Type": "application/json"}

    response = requests.request("GET", url, headers=headers, data=payload)

    logging.info(response.text)
    return json.loads(response.text)


def get_sub_areas_list(size):
    logging.info(f"get_sub_areas_list {size}")
    url = config.endpoint_url
    payload = json.dumps(
        {
            "version": True,
            "size": size,
            "sort": [{"_score": {"order": "desc"}}],
            "query": {
                "bool": {
                    "must": [],
                    "filter": [
                        {"match_all": {}},
                        {"exists": {"field": "subject_areas.crossref"}},
                    ],
                    "should": [],
                    "must_not": [],
                }
            },
            "_source": ["subject_areas.crossref"],
        }
    )
    headers = {"Content-Type": "application/json"}
    final_subjects = []
    try:
        response = requests.request("GET", url, headers=headers, data=payload)
        data = json.loads(response.text)
        for index in data["hits"]["hits"]:
            final_subjects.append(index["_source"]["subject_areas"]["crossref"])

        flat_list = [item for sublist in final_subjects for item in sublist]
        return flat_list
    except Exception as ex:
        logging.info(ex)
        return ""
