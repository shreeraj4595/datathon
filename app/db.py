import psycopg2
import config

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
        print("PostgreSQL connection is opened")
        return conn.cursor()
    except Exception as ex:
        print(ex)
        return ""


def get_subject_data(limit, offset, where, year):
    print(f"get_subject_data {limit}, {offset}, {where}, {year}")
    final_data = {}
    cursor = connect()
    if cursor == "":
        return ""
    try:
        if where == "":
            where = ""
        else:
            where = "and a.subject_areas_crossref_0='" + where + "'"
        if len(year) == 0:
            year = ["2022", "2021", "2020", "2019", "2018"]
        query = (
            "select a.dates_pub, a.dates_accepted, a.dates_online, p.publisher_name_ui, a.subject_areas_crossref_0, date_part('year', a.dates_pub) as pub_year",
            "from Artifacts a "
            "inner join publisher p on a.publisher_id = p.publisher_id inner join Journal j on a.journal_id=j.journal_id "
            "where date_part('year', a.dates_pub) in (" + ", ".join(year) + ") "
            "and j.journal_name is not NULL and a.dates_online is not NULL and a.dates_accepted is not NULL "
            "and a.dates_accepted is not NULL "
            + where
            + " and a.top_concepts_0 is not NULL limit "
            + str(limit)
            + " offset "
            + str(offset),
        )
        cursor.execute(" ".join(query))
        subject_records = cursor.fetchall()
        index = 0
        for row in subject_records:
            return_list = {}
            # return_list["dates_pub"] = row[0]
            # return_list["dates_accepted"] = row[1]
            # return_list["dates_online"] = row[2]
            return_list["publisher_name_ui"] = row[3]
            return_list["subject_areas_crossref_0"] = row[4]
            return_list["dates_publ_minus_accepted_days"] = (row[0] - row[1]).days
            return_list["dates_publ_minus_accepted_month"] = round(
                int((row[0] - row[1]).days) / 30, 2
            )
            return_list["pub_year"] = row[5]
            final_data[index] = return_list
            index = index + 1

        cursor.close()
        return final_data
    except Exception as ex:
        print(f"Exception in get_subject_data {ex}")
        return ""
    finally:
        if conn:
            cursor.close()
            conn.close()
            print("PostgreSQL connection is closed")


def get_subject_data_list(limit, offset):
    try:
        print(f"get_subject_data_list {limit}")
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
        print(f"Exception in get_subject_data_list {ex}")
        return ""
    finally:
        if conn:
            cursor.close()
            conn.close()
            print("PostgreSQL connection is closed")


def get_country_data(limit, offset, where, year):
    print(f"get_country_data {limit}, {offset}, {where}, {year}")
    final_data = {}
    cursor = connect()
    if cursor == "":
        return ""
    try:
        if where == "":
            where = ""
        else:
            where = (
                "and auth.authors_0_aff_address_country ='" + where.capitalize() + "'"
            )
        if len(year) == 0:
            year = ["2022", "2021", "2020", "2019", "2018"]
        query = (
            "select a.top_concepts_0, a.title, a.dates_pub, a.dates_accepted, a.dates_online, auth.authors_0_aff_address_country ",
            "from Artifacts a "
            "inner join authors auth on a.dyson_id = auth.dyson_id "
            "where date_part('year', a.dates_pub) in (" + ", ".join(year) + ") "
            "and a.dates_online is not NULL and a.dates_accepted is not NULL "
            "and a.dates_accepted is not NULL and auth.authors_0_aff_address_country is not NULL "
            + where
            + " and a.top_concepts_0 is not NULL limit "
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
            return_list["country"] = row[5]
            return_list["dates_publ_minus_accepted_days"] = (row[2] - row[3]).days
            return_list["dates_publ_minus_accepted_month"] = round(
                int((row[2] - row[3]).days) / 30, 2
            )
            final_data[index] = return_list
            index = index + 1

        cursor.close()
        return final_data
    except Exception as ex:
        print(f"Exception in get_country_data {ex}")
        return ""
    finally:
        if conn:
            cursor.close()
            conn.close()
            print("PostgreSQL connection is closed")


def get_country_list(limit, offset):
    try:
        print(f"get_country_list {limit}")
        final_data = []
        cursor = connect()
        if cursor == "":
            return ""
        query = (
            "select distinct authors_0_aff_address_country from Authors where authors_0_aff_address_country is not NULL limit "
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
        print(f"Exception in get_country_list {ex}")
        return ""
    finally:
        if conn:
            cursor.close()
            conn.close()
            print("PostgreSQL connection is closed")
        
def get_publisher_list(limit, offset):
    try:
        print(f"get_publisher_list {limit}")
        final_data = []
        cursor = connect()
        if cursor == "":
            return ""
        query = (
            "select distinct publisher from Publisher where publisher is not NULL limit "
            + str(limit)
            + " offset "
            + str(offset),
        )
        cursor.execute(" ".join(query))
        subject_list = cursor.fetchall()
        for row in subject_list:
            row=row[0].split(",")[1]
            row=row[1:-1]
            final_data.append(row)

        cursor.close()
        return final_data
    except Exception as ex:
        print(f"Exception in get_publisher_list {ex}")
        return ""
    finally:
        if conn:
            cursor.close()
            conn.close()
            print("PostgreSQL connection is closed")

def get_journal_list(limit, offset):
    try:
        print(f"get_journal_list {limit}")
        final_data = []
        cursor = connect()
        if cursor == "":
            return ""
        query = (
            "select distinct clean_journal_name from Journal where clean_journal_name is not NULL limit "
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
        print(f"Exception in get_journal_list {ex}")
        return ""
    finally:
        if conn:
            cursor.close()
            conn.close()
            print("PostgreSQL connection is closed")