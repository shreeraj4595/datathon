import config
import psycopg2
import logging
from logging.handlers import RotatingFileHandler

logging.basicConfig(
    handlers=[RotatingFileHandler("app.log", maxBytes=100000, backupCount=10)],
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
)
conn = ""


def connect():
    try:
        global conn
        conn = psycopg2.connect(
            database=config.db_database,
            host=config.db_host,
            user=config.db_username,
            password=config.db_password,
            port=config.db_port,
        )
        logging.info("PostgreSQL connection is opened")
        return conn.cursor()
    except Exception as ex:
        logging.info(ex)
        return ""


def get_subject_data(limit, offset, where):
    logging.info(f"get_subject_data {limit}, {offset}, {where}")
    final_data = {}
    cursor = connect()
    if cursor == "":
        return ""
    try:
        query = (
            "select a.top_concepts_0, a.title, a.dates_pub, a.dates_accepted, a.dates_online, p.publisher_name_ui, j.journal_name, a.subject_areas_crossref_0, a.dyson_id ",
            "from Artifacts a "
            "inner join publisher p on a.publisher_id = p.publisher_id inner join Journal j on a.journal_id=j.journal_id "
            "where date_part('year', a.dates_pub) in ('2022', '2021', '2020', '2019', '2018', '2017') "
            "and j.journal_name is not NULL and a.dates_online is not NULL and a.dates_accepted is not NULL "
            "and a.dates_accepted is not NULL and a.subject_areas_crossref_0 LIKE '"
            + where.capitalize()
            + "%' and a.top_concepts_0 is not NULL order by a.dyson_id limit "
            + str(limit)
            + " offset "
            + str(offset),
        )
        cursor.execute(" ".join(query))
        subject_records = cursor.fetchall()
        index = 0
        for row in subject_records:
            return_list = {}
            return_list["paper"] = row[0]
            return_list["title"] = row[1]
            return_list["dates_pub"] = row[2]
            return_list["dates_accepted"] = row[3]
            return_list["dates_online"] = row[4]
            return_list["publisher_name_ui"] = row[5]
            return_list["journal_name"] = row[6]
            return_list["subject_areas_crossref_0"] = row[7]
            return_list["dates_publ_minus_accepted_days"] = (row[2] - row[3]).days
            return_list["dates_publ_minus_accepted_month"] = (
                int((row[2] - row[3]).days) / 30
            )
            return_list["dyson_id"] = row[8]
            final_data[index] = return_list
            index = index + 1
            # if return_list not in final_data:
            #     pass
            # else:
            # final_data.append(return_list.copy())

        cursor.close()
        return final_data
    except Exception as ex:
        logging.info(f"Exception in get_subject_data {ex}")
        return ""
    finally:
        if conn:
            cursor.close()
            conn.close()
            logging.info("PostgreSQL connection is closed")


def get_subject_data_list(limit, offset):
    try:
        logging.info(f"get_subject_data_list {limit}")
        final_data = []
        cursor = connect()
        if cursor == "":
            return ""
        query = (
            "select distinct subject_areas_crossref_0 from Artifacts where subject_areas_crossref_0 is not NULL limit "
            + str(limit)
            + " offset "
            + str(offset),
        )
        cursor.execute(" ".join(query))
        subject_list = cursor.fetchall()
        for row in subject_list:
            final_data.append(row[0])

        cursor.close()
        return final_data
    except Exception as ex:
        logging.info(f"Exception in get_subject_data_list {ex}")
        return ""
    finally:
        if conn:
            cursor.close()
            conn.close()
            logging.info("PostgreSQL connection is closed")
