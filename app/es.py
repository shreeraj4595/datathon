import json
import requests
import config
import datetime

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

    print(response.text)
    return json.loads(response.text)


def get_sub_areas_list(size):
    print(f"get_sub_areas_list {size}")
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
        print(ex)
        return ""

def get_publisher_list(size):
    print(f"get_publisher_list {size}")
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
                        {"exists": {"field": "publisher"}},
                    ],
                    "should": [],
                    "must_not": [],
                }
            },
            "_source": ["publisher"],
        }
    )
    headers = {"Content-Type": "application/json"}
    final_subjects = []
    try:
        response = requests.request("GET", url, headers=headers, data=payload)
        data = json.loads(response.text)
        for index in data["hits"]["hits"]:
            final_subjects.append(index["_source"]["publisher"])

        # flat_list = [item for sublist in final_subjects for item in sublist]
        return final_subjects
    except Exception as ex:
        print(ex)
        return ""

def get_journal_list(size):
    print(f"get_journal_list {size}")
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
                        {"exists": {"field": "journal_name"}},
                    ],
                    "should": [],
                    "must_not": [],
                }
            },
            "_source": ["journal_name"],
        }
    )
    headers = {"Content-Type": "application/json"}
    final_subjects = []
    try:
        response = requests.request("GET", url, headers=headers, data=payload)
        data = json.loads(response.text)
        for index in data["hits"]["hits"]:
            final_subjects.append(index["_source"]["journal_name"])

        # flat_list = [item for sublist in final_subjects for item in sublist]
        return final_subjects
    except Exception as ex:
        print(ex)
        return ""
        
def get_sub_area_data(size, from_year, to_year, sub_area ):
    print(f"get_sub_area_data {size}")
    url = config.endpoint_url

    from_year = from_year + "-01-01"
    to_year = to_year + "-12-31"
    payload = json.dumps(
        {
            "version": True,
            "size": size,
            "sort": [{"_score": {"order": "asc"}}],
            "query": {
                "bool": {
                    "must": [],
                    "filter": [
                        {"match_all": {}},
                        {"exists": {"field": "dates_accepted"}},
                        {
                            "range": {
                                "dates_pub": {"gte": from_year, "lt": to_year}
                            }
                        },
                    ],
                    "should": [{"match_phrase": {"subject_areas.crossref": sub_area}}],
                    "minimum_should_match": 1,
                    "must_not": [],
                }
            },
            "_source": [
                "subject_areas.crossref",
                "dates_pub",
                "dates_accepted",
                "dates_online",
                "publisher_name_ui",
            ],
        }
    )
    headers = {"Content-Type": "application/json"}
    final_data = {}
    try:
        response = requests.request("GET", url, headers=headers, data=payload)
        data = json.loads(response.text)
        index = 0
        format = '%Y-%m-%d'

        for ind in data["hits"]["hits"]:
            return_list = {}
            for i, j in enumerate(ind["_source"]["subject_areas"]["crossref"]):
                if j == sub_area:
                    if "dates_pub" in ind["_source"] and "dates_accepted" in ind["_source"]:
                        publ = datetime.datetime.strptime(ind["_source"]["dates_pub"], format)
                        accpt = datetime.datetime.strptime(ind["_source"]["dates_accepted"], format)
                        return_list["subject_areas_crossref_0"] = sub_area              
                        return_list['dates_pub'] = ind["_source"]["dates_pub"]
                        return_list['dates_accepted'] = ind["_source"]["dates_accepted"] 
                        return_list['publisher_name_ui'] = ind["_source"]["publisher_name_ui"]
                        return_list["dates_publ_minus_accepted_days"] = (publ - accpt).days
                        return_list["dates_publ_minus_accepted_month"] = round(
                            int((publ - accpt).days) / 30, 2
                        )
                        return_list['pub_year'] = publ.year
                        final_data[index] = return_list
                        index = index + 1
                    else:
                        continue  
            
        return final_data
    except Exception as ex:
        print(ex)
        return ""
