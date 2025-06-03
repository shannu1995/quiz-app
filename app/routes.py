from app import app
from flask import render_template, request, session, jsonify
import json
import pandas as pd
import requests
from datetime import datetime
from io import StringIO
import sqlite3
import os
from config import Config
import random
from app.helpers import return_existing_data, get_capitals_quiz_data, get_connection
import psycopg2
from urllib.parse import urlparse


@app.route('/env')
def show_env():
    db = os.environ.get('DATABASE_URL', 'DATABASE_URL not set')
    if db.__contains__('postgres'):
        conn = psycopg2.connect(db)
        conn = psycopg2.connect(db)
        conn.close()
        return "Connected to PostgreSQL database"
    return db
@app.route('/')
@app.route('/index')
def index():
    title = "Georgraphy Quiz App"
    return render_template('index.html', title=title)

@app.route('/view-existing-data', methods=['GET'])
def view_existing_data():
    if return_existing_data():
        with get_connection() as conn:
            capitals_quiz_data = pd.read_sql_query(f"SELECT * FROM {Config.CAPITALS_TABLE_NAME}", conn)
            last_updated = capitals_quiz_data["Last Updated"].iloc[0]
        return render_template('view-existing-data.html', data=capitals_quiz_data.to_html(), date=last_updated)
    else:
        return render_template('no-data.html', data="No data available. Unable to connect to the database. ")
    
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

@app.route('/capitals-quiz', methods=['GET', 'POST'])
def capitals_quiz():
    difficulty = request.form.get('difficulty')
    continent = request.form.get('continent')
    capitals_quiz_data = get_capitals_quiz_data()
    if difficulty:
        print(f"Difficulty: {difficulty}")
        filter_type = "difficulty"
        if difficulty == "random":
            quiz_data = capitals_quiz_data.sample(5)
        elif difficulty == "easy":
            quiz_data = capitals_quiz_data.head(5)
        elif difficulty == "hard":
            capitals_quiz_data_difficulty_filter = capitals_quiz_data.tail(50)
            quiz_data = capitals_quiz_data_difficulty_filter.sample(5)
        countries = list(quiz_data['Country/Territory'])
        correct_cities = tuple(zip(quiz_data["City/Town"], quiz_data["Country/Territory"]))
        session['correct_cities'] = json.dumps(correct_cities)
        scrambled_cities = random.sample(correct_cities, len(correct_cities))
        return render_template('capitals-quiz.html', filter_value=difficulty, filter_type=filter_type, countries=countries, scrambled_cities=scrambled_cities)
    else:
        filter_type = "continent"
        quiz_data = capitals_quiz_data[capitals_quiz_data['Continent'] == continent].copy()
        quiz_data = quiz_data.sample(10) if len(quiz_data) > 10 else quiz_data
        countries = list(quiz_data['Country/Territory'])
        correct_cities = tuple(zip(quiz_data["City/Town"], quiz_data["Country/Territory"]))
        session['correct_cities'] = json.dumps(correct_cities)
        scrambled_cities = random.sample(correct_cities, len(correct_cities))
        return render_template('capitals-quiz.html', filter_value=continent, filter_type=filter_type, countries=countries, scrambled_cities=scrambled_cities)
@app.route('/submit_results', methods=['POST'])
def submit_results():
    user_answers = request.get_json()
    session['user_answers'] = json.dumps(user_answers)
    return jsonify({'redirect_url': '/check_matches'})
@app.route('/check_matches')
def check_matches():
    user_matches = json.loads(session.get('user_answers', '{}'))
    correct_cities = json.loads(session.get('correct_cities', '[]'))
    inverted_matches = {
        country.strip().lower(): capital.strip()
        for capital, country in user_matches.items()
    }

    results = []
    for correct_city, country in correct_cities:
        user_city = inverted_matches.get(country.strip().lower())
        results.append({
            'country': country,
            'user_city': user_city,
            'correct_city': correct_city,
            'is_correct': user_city == correct_city
        })
    return render_template('check_matches.html', data=results)