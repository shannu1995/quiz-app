from app import app
from flask import render_template, url_for
import pandas as pd
import requests
from datetime import datetime
from io import StringIO
import sqlite3
import os
from config import Config

@app.route('/')
@app.route('/index')
def index():
    title = "Georgraphy Quiz App"
    return render_template('index.html', title=title)

@app.route('/view-existing-data', methods=['GET'])
def view_existing_data():
    if not os.path.exists(Config.DB_PATH):
        return render_template('no-data.html', data="No data available. Database file does not exist.")
    try:
        with sqlite3.connect(Config.DB_PATH) as conn:
            capitals_quiz_data = pd.read_sql_query(f"SELECT * FROM {Config.CAPITALS_TABLE_NAME}", conn)
            last_updated = capitals_quiz_data["Last Updated"].iloc[0]
        return render_template('view-existing-data.html', data=capitals_quiz_data.to_html(), date=last_updated)
    except Exception as e:
        return render_template('no-data.html', data="No data available. Unable to connect to the database. " + e)
    
@app.route('/refresh-data', methods=['GET'])
def refresh_table_data():
    popular_pages_url = "https://en.wikipedia.org/wiki/Wikipedia:WikiProject_Countries/Popular_pages"
    request_1 = requests.get(popular_pages_url)
    popularity_data = StringIO(request_1.text)
    popularity_df = pd.read_html(popularity_data)[0]
    national_capitals_url = "https://en.wikipedia.org/wiki/List_of_national_capitals"
    request_2 = requests.get(national_capitals_url)
    capitals_data = StringIO(request_2.text)
    capitals_df = pd.read_html(capitals_data)[1]
    capitals_quiz_data = pd.merge(popularity_df, capitals_df, how='inner', left_on='Page title', right_on='Country/Territory')
    capitals_quiz_data_relevant_only = capitals_quiz_data[['Country/Territory', 'City/Town', "Continent", "Views"]].copy()
    capitals_quiz_data_relevant_only["Last Updated"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with sqlite3.connect(Config.DB_PATH) as conn:
        capitals_quiz_data_relevant_only.to_sql(Config.CAPITALS_TABLE_NAME, conn, if_exists='replace', index=False)
    return render_template('refresh-data.html', data=capitals_quiz_data_relevant_only.to_html())