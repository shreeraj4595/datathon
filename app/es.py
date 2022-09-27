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
                "journal_name"
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
        minimum, actual_min, avg = 0, 0, 0.0
        maximum = 0

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
                        return_list['journal_name'] = ind["_source"]["journal_name"] if "journal_name" in ind["_source"] else ""
                        return_list["dates_publ_minus_accepted_days"] = (publ - accpt).days
                        return_list["dates_publ_minus_accepted_month"] = round(
                            int((publ - accpt).days) / 30, 2
                        )
                        return_list['pub_year'] = publ.year
                        final_data[index] = return_list
                        index = index + 1
                    else:
                        continue
                    
                    if (return_list["dates_publ_minus_accepted_days"] < minimum and return_list["dates_publ_minus_accepted_days"] > 0) or minimum == 0:
                        minimum =  return_list["dates_publ_minus_accepted_days"]
                    if return_list["dates_publ_minus_accepted_days"] > maximum:
                        maximum = return_list["dates_publ_minus_accepted_days"]
                    if return_list["dates_publ_minus_accepted_days"] < minimum or minimum == 0:
                        actual_min = return_list["dates_publ_minus_accepted_days"]
        final_data['maximum_days'] = maximum
        final_data['minimum_days'] = minimum
        final_data['actual_minimum_days'] = actual_min
        final_data['avg_days'] = round(int(maximum + minimum) / (len(final_data) - 3), 2)
        return final_data
    except Exception as ex:
        print(ex)
        return ""

def get_journal_data(size, from_year, to_year, journal, publisher ):
    print(f"get_journal_data {size}, {from_year}, {to_year}, {journal}")
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
                    # "should": [{"match_phrase": {"journal_name": journal}}],
                    # "minimum_should_match": 1,
                    "must_not": [],
                }
            },
            "_source": [
                "dates_pub", "dates_accepted", "dates_online", "publisher_name_ui", "journal_name"
            ],
        }
    )
    headers = {"Content-Type": "application/json"}
    if journal != "" and publisher == "":
        add_journal = [{"match_phrase": {"journal_name": journal}}]
        temp = json.loads(payload)
        temp['query']['bool']['should'] = add_journal
        temp['query']['bool']['minimum_should_match'] = 1
        payload = json.dumps(temp)
    elif journal == "" and publisher != "":
        add_pub = [{"match_phrase": {"publisher_name_ui": publisher}}]
        temp = json.loads(payload)
        temp['query']['bool']['should'] = add_pub
        temp['query']['bool']['minimum_should_match'] = 1
        payload = json.dumps(temp)
    final_data = {}
    try:
        response = requests.request("GET", url, headers=headers, data=payload)
        data = json.loads(response.text)
        index = 0
        format = '%Y-%m-%d'

        for ind in data["hits"]["hits"]:
            return_list = {}
            for i, j in enumerate(ind["_source"]):
                    if "dates_pub" in ind["_source"] and "dates_accepted" in ind["_source"]:
                        publ = datetime.datetime.strptime(ind["_source"]["dates_pub"], format)
                        accpt = datetime.datetime.strptime(ind["_source"]["dates_accepted"], format)
                        return_list["journal_name"] = ind["_source"]["journal_name"] if "journal_name" in ind["_source"] else ""             
                        return_list['dates_pub'] = ind["_source"]["dates_pub"]
                        return_list['dates_accepted'] = ind["_source"]["dates_accepted"] 
                        return_list['publisher_name_ui'] = ind["_source"]["publisher_name_ui"] if "publisher_name_ui" in ind["_source"] else ""
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
