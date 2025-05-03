import psycopg2
import uuid
from datetime import datetime, timezone
from zoneinfo import ZoneInfo


def existsTable(cursor):
    try:
        cursor.execute("""
            SELECT EXISTS(
                SELECT FROM pg_tables
                    WHERE tablename = %s
            )
        """, ("healthxuser_crud", ))

        return cursor.fetchone()[0]
    except psycopg2.Error as exce:
        print(
            f"An error occured during check users CRUD table exists : {exce}")


def createTable(database, cursor):
    try:
        cursor.execute("""
            CREATE TABLE healthxuser_crud (
                    id VARCHAR(50) PRIMARY KEY UNIQUE NOT NULL,
                    username VARCHAR(10) NOT NULL,
                    patient_name VARCHAR(30),
                    gender VARCHAR(7),
                    disease VARCHAR(20),
                    phone VARCHAR(16),
                    address VARCHAR(20),
                    date VARCHAR(30) NOT NULL,
                       
                    FOREIGN KEY (userName) REFERENCES healthxuser(userName)
                )
            """)

        cursor.execute("""
                CREATE INDEX index_id ON healthxuser_crud(id)
            """)

        database.commit()

    except psycopg2.Error as exce:
        print(f"An error occured during creating users CRUD table : {exce}")


def createSingleUserTask(database, cursor, userName, exists, requestedData):
    try:
        if exists is False:
            createTable(database, cursor)

        if requestedData != {}:
            id = str(uuid.uuid1())
            patientName = requestedData["patientName"]
            gender = requestedData["gender"]
            disease = requestedData["disease"]
            phone = requestedData["phone"]
            address = requestedData["address"]
            datee = str(datetime.now(ZoneInfo("Asia/Dhaka"))).split(" ")
            datee = datee[0] + " " + datee[1].split(".")[0]

            cursor.execute("""
                INSERT INTO healthxuser_crud 
                    (id, username, patient_name, gender, disease, phone, address, date)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
            """, (id, userName, patientName, gender, disease, phone, address, datee, ))

            database.commit()

    except psycopg2.Error as exce:
        print(
            f"An error occured during creating database users CRUD table: {exce}")


def readAll(database, cursor):
    try:
        exists = existsTable(cursor)
        if exists is False:
            createSingleUserTask(database, cursor, "", exists, {})

    except psycopg2.Error as exce:
        print(f"An error occured during read all user CRUD Task: {exce}")


def readAllSingleUserTask(cursor, userName):
    try:
        cursor.execute("""
            SELECT id, patient_name, gender, disease, phone, address, date
                FROM healthxuser_crud WHERE username = %s;
        """, (userName, ))

        fetchAllData = cursor.fetchall()

        return fetchAllData

    except psycopg2.Error as exce:
        print(f"An error occured during read users Task: {exce}")


def updateSingleUserTask(database, cursor, userName, taskId, requestedData):

    try:
        patient_name = requestedData["patientName"]
        gender = requestedData["gender"]
        disease = requestedData["disease"]
        phone = requestedData["phone"]
        address = requestedData["address"]

        cursor.execute("""
            UPDATE healthxuser_crud SET 
                    patient_name = %s,
                    gender = %s,
                    disease = %s,
                    phone = %s,
                    address = %s
                WHERE username = %s AND id = %s
        """, (patient_name, gender, disease, phone, address, userName, taskId, ))

        database.commit()

    except psycopg2.Error as exce:
        print(f"An error occured during update users Task: {exce}")


def deleteSingleUserTask(database, cursor, taskId):
    try:
        cursor.execute("""
            DELETE FROM healthxuser_crud WHERE id = %s;
        """, (taskId, ))

    except psycopg2.Error as exce:
        print(f"An error occured during delete users Task: {exce}")
