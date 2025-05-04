import psycopg2
import bcrypt


def existsTable(cursor):
    try:
        cursor.execute("""
            SELECT EXISTS(
                SELECT FROM pg_tables
                    WHERE tablename=%s
            )
        """, ("healthxuser", ))

        return cursor.fetchone()[0]
    except psycopg2.Error as exce:
        print(f"An error occured during check table exists : {exce}")


def createTable(database, cursor):
    try:
        cursor.execute("""
            CREATE TABLE healthxuser (
                    username VARCHAR(100) PRIMARY KEY UNIQUE NOT NULL,
                    password VARCHAR(400) NOT NULL
                )
            """)

        cursor.execute("""
                CREATE INDEX index_username ON healthxuser(username)
            """)

        database.commit()

    except psycopg2.Error as exce:
        print(f"An error occured during creating users table : {exce}")


def createUser(database, cursor, exists, requestedData):
    try:
        if exists is False:
            createTable(database, cursor)

        if requestedData != {}:
            # Storing hased password
            password = bcrypt.hashpw(
                requestedData["password"].encode(), bcrypt.gensalt()).decode()

            cursor.execute("""
                INSERT INTO healthxuser (username, password) 
                    VALUES (%s, %s);
            """, (requestedData["userName"], password, ))

            database.commit()

    except psycopg2.Error as exce:
        print(f"An error occured during creating database table: {exce}")


def readAllUser(database, cursor):
    try:
        exists = existsTable(cursor)
        if exists is False:
            createUser(database, cursor, exists, {})

    except psycopg2.Error as exce:
        print(f"An error occured during read all user: {exce}")


def readSingleUser(cursor, userName):
    try:
        cursor.execute("""
            SELECT userName FROM healthxuser WHERE username=%s;
        """, (userName, ))

        return cursor.fetchone()
    except psycopg2.Error as exce:
        print(f"An error occured during read single user: {exce}")


def readSingleUser_Password(cursor, requestedData):
    cursor.execute("""
        SELECT username, password FROM healthxuser WHERE username = %s;
    """, (requestedData["userName"], ))
    
    password = cursor.fetchone()

    if password is None:
        return None

    checkHasedPassword = bcrypt.checkpw(
        requestedData["password"].encode(), password[1].encode())

    if checkHasedPassword is False:
        return None

    return True
