from app import app
from flask import render_template

@app.errorhandler(404)
def not_found_error(error):
    print()
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    print()
    return render_template('500.html'), 500