from fastapi import FastAPI, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
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

@app.get("/getPublishedDate")
async def get_date_difference():
    '''
    THIS API IS ONLY FOR DEV PURPOSE
    '''
    return es.get_dates_diff()


@app.get("/getSubjectAreaData", status_code=200)
async def get_subject_data(limit: int = 100, sub_area: str = "", skip: int = 0):
    """
    This API is used to query the set of data from Artifacts table.
    limit is default to 100, can be passed other values from the caller
    sub area can be queried for particular value not mandatory
    skip is the offset to specify from what record to query for default to 0
    """
    ret = db.get_subject_data(limit, skip, sub_area)
    if ret == "":
        # return {
        #     "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
        #     "message": "Oops! Something went wrong",
        # }
        raise HTTPException(status_code=500, detail="Oops! Something went wrong")
    # print(ret)
    return ret


@app.get("/getSubjectArea", status_code=200)
async def get_subject_list(limit: int = 100, skip: int = 0, query_from: str = "db"):
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
        # return {
        #     "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
        #     "message": "Oops! Something went wrong",
        # }
        raise HTTPException(status_code=500, detail="Oops! Something went wrong")
    # print(ret)
    return ret

@app.get("/getCountryWiseData", status_code=200)
async def get_country_data(limit: int = 100, country: str = "", skip: int = 0):
    """
    This API is used to query the set of data from authors and artifacts table.
    limit is default to 100, can be passed other values from the caller
    country can be queried for particular value not mandatory
    skip is the offset to specify from what record to query for default to 0
    """
    ret = db.get_country_data(limit, skip, country)
    if ret == "":
        # return {
        #     "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
        #     "message": "Oops! Something went wrong",
        # }
        raise HTTPException(status_code=500, detail="Oops! Something went wrong")
    # print(ret)
    return ret


# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8082)
