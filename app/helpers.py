import sqlite3
import pandas as pd
import os
from config import Config
import psycopg2
from sqlalchemy import create_engine

def get_connection():
    database_url = os.environ.get("DATABASE_URL")
    if database_url.__contains__('postgres'):
        import urllib.parse as urlparse
        url = urlparse.urlparse(database_url)
        conn = psycopg2.connect(
            dbname=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port
        )
        return conn
    else:
        return sqlite3.connect(Config.DB_PATH)
def get_alchemy_connection():
    database_url = os.environ.get("DATABASE_URL")
    if database_url:
        return create_engine(database_url)
    else:
        return create_engine(f"sqlite:///{Config.DB_PATH}")
    
def return_existing_data():
    try:
        with get_connection() as conn:
            capitals_quiz_data = pd.read_sql_query(f"SELECT * FROM {Config.CAPITALS_TABLE_NAME}", conn)
            return True
    except Exception as e:
        return False

def get_capitals_quiz_data():
    with get_connection() as conn:
        capitals_quiz_data = pd.read_sql_query(f"SELECT * FROM {Config.CAPITALS_TABLE_NAME}", conn)
    return capitals_quiz_data