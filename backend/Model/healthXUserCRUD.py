import psycopg2
import uuid


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

            print("id : ", id)

            cursor.execute("""
                INSERT INTO healthxuser_crud (id, username, patient_name, gender, disease, phone, address)
                    VALUES (%s, %s, %s, %s, %s, %s, %s);
            """, (id, userName, patientName, gender, disease, phone, address, ))

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
            SELECT id, patient_name, gender, disease, phone, address
                FROM healthxuser_crud WHERE username = %s;
        """, (userName, ))

        fetchAllData = cursor.fetchall()

        return fetchAllData

    except psycopg2.Error as exce:
        print(f"An error occured during read users Task: {exce}")
