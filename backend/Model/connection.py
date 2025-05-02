from dotenv import load_dotenv
import psycopg2
import sys
import os

load_dotenv(os.path.join(os.path.dirname(__file__), "../.env"))


def createConnection():
    url = os.getenv("DEVELOPMENT_DATABASE_URL") if sys.argv[1] == "development" else os.getenv(
        "PRODUCTION_DATABASE_URL")

    connect = psycopg2.connect(url)

    print("Connection Created")
    return connect
