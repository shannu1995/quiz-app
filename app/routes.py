from app import app
from flask import render_template, url_for

@app.route('/')
@app.route('/index')
def index():
    title = "Georgraphy Quiz App"
    return render_template('index.html', title=title)