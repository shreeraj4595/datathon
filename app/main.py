from typing import List
from fastapi import FastAPI, status, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from pydantic import BaseModel
from typing import List
import es
import db

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class DataModelIn(BaseModel):
    limit: int = 100
    sub_area: str = ""
    skip: int = 0
    country: str = ""
    year: List[str] = []


@app.get("/getPublishedDate")
async def get_date_difference():
    """
    THIS API IS ONLY FOR DEV PURPOSE
    """
    return es.get_dates_diff()

@app.post("/getSubjectAreaData", status_code=200)
async def get_subject_data(request: Request, data: DataModelIn):
    """
    This API is used to query the set of data from Artifacts table.
    limit is default to 100, can be passed other values from the caller.
    sub area can be queried for particular value not mandatory.
    skip is the offset to specify from what record to query for default to 0.
    pass country as empty string.
    year is a list of string eg: ['2022','2020']
    """
    if data.country != "":
        raise HTTPException(
            status_code=400, detail="Country param is invalid in this API"
        )
    ret = db.get_subject_data(data.limit, data.skip, data.sub_area, data.year, request)
    if ret == "":
        raise HTTPException(status_code=500, detail="Oops! Something went wrong")
    return ret

@app.get("/getSubjectAreaData", status_code=200)
async def get_subject_data_get(request: Request, limit: int = 100, skip: int = 0, sub_area: str = "", year: str = "", query_from: str = "es"):
    """
    This API is used to query the set of data from Artifacts table.
    limit is default to 100, can be passed other values from the caller.
    sub area can be queried for particular value not mandatory but MANDATORY FOR QUERYING FROM ES.
    skip is the offset to specify from what record to query for default to 0, SKIP NOT USED IN ES.
    year is a string which is not mandatory for db but MANDATORY FOR ES
    """
    if query_from == "db":
        ret = db.get_subject_data(limit, skip, sub_area, year, request.method)
    else:
        if sub_area == "" or year == "":
            raise HTTPException(status_code=400, detail="Subject Area and Year are the mandatory fields")
        ret = es.get_sub_area_data(limit,  year,  year, sub_area)
    if ret == "":
        raise HTTPException(status_code=500, detail="Oops! Something went wrong")
    return ret

@app.get("/getSubjectArea", status_code=200)
async def get_subject_list(limit: int = 100, skip: int = 0, query_from: str = "es"):
    """
    This API is used to get the list of subject area. This DB query takes lot of time, use with caution and only if necessary
    limit is default to 100, can be passed other values from the caller. Give query_from as "es" to query from Elastic Search
    skip is the offset to specify from what record to query for default to 0
    """
    if query_from == "db":
        ret = db.get_subject_data_list(limit, skip)
    else:
        ret = es.get_sub_areas_list(limit)
    if ret == "":
        raise HTTPException(status_code=500, detail="Oops! Something went wrong")
    # print(ret)
    return ret

@app.post("/getCountryWiseData", status_code=200)
async def get_country_data(data: DataModelIn):
    """
    This API is used to query the set of data from authors and artifacts table.
    limit is default to 100, can be passed other values from the caller.
    country can be queried for particular value not mandatory.
    skip is the offset to specify from what record to query for default to 0.
    pass sub area as empty string.
    year is a list of string eg: ['2022','2020'].
    """
    if data.sub_area != "":
        raise HTTPException(
            status_code=400, detail="Sub Area param is invalid in this API"
        )
    ret = db.get_country_data(data.limit, data.skip, data.country, data.year)
    if ret == "":
        raise HTTPException(status_code=500, detail="Oops! Something went wrong")
    return ret

@app.get("/getCountryList", status_code=200)
async def get_country_list(limit: int = 100, skip: int = 0):
    """
    This API is used to get the list of Country.
    """
    ret = db.get_country_list(limit, skip)
    if ret == "":
        raise HTTPException(status_code=500, detail="Oops! Something went wrong")
    return ret

@app.get("/getPublisherList", status_code=200)
async def get_publisher_list(limit: int = 100, skip: int = 0,query_from: str = "es"):
    """
    This API is used to get the list of Country.
    """
    if query_from == "db":
        ret = db.get_publisher_list(limit, skip)
    else:
        ret = es.get_publisher_list(limit)

    if ret == "":
        raise HTTPException(status_code=500, detail="Oops! Something went wrong")
    return ret

@app.get("/getJournalList", status_code=200)
async def get_journal_list(limit: int = 100, skip: int = 0,query_from: str = "es"):
    """
    This API is used to get the list of Country.
    """
    if query_from == "db":
        ret = db.get_journal_list(limit, skip)
    else:
        ret = es.get_journal_list(limit)
    if ret == "":
        raise HTTPException(status_code=500, detail="Oops! Something went wrong")
    return ret

@app.get("/getPubJournalData", status_code=200)
async def get_pub_journal_data(request: Request, limit: int = 100, skip: int = 0, journal: str = "", year: str = "", query_from: str = "es", publisher: str = ""):
    """
    This API is used to query the set of data from ES.
    limit is default to 100, can be passed other values from the caller.
    journal name can be queried for particular value not mandatory.
    skip is the offset to specify from what record to query for default to 0, SKIP NOT USED IN ES.
    year is a string which is not mandatory for db but MANDATORY FOR ES
    QUERYING FROM DATABASE IS NOT DONE FOR THIS API.
    """
    if query_from == "db":
        raise HTTPException(status_code=501, detail="The API does not support the funcationality required to fulfill the request")
        ret = db.get_subject_data(limit, skip, journal, year, request.method)
    else:
        if journal != "" and publisher != "":
            raise HTTPException(status_code=400, detail="Journal and Publisher both can't be queried at once. Pls request anyone")
        if year == "":
            raise HTTPException(status_code=400, detail="Year is a mandatory field")
        ret = es.get_journal_data(limit,  year,  year, journal, publisher)
    if ret == "":
        raise HTTPException(status_code=500, detail="Oops! Something went wrong")
    return ret

# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8082)
