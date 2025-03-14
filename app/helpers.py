import sqlite3
import pandas as pd
import os
from config import Config
def return_existing_data():
    try:
        with sqlite3.connect(Config.DB_PATH) as conn:
            capitals_quiz_data = pd.read_sql_query(f"SELECT * FROM {Config.CAPITALS_TABLE_NAME}", conn)
            return True
    except Exception as e:
        return False