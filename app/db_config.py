import os

db = os.environ.get('DATABASE_URL', 'DATABASE_URL not set')

if "postgres" in db:
    DB_TYPE = "postgres"
    column_names = {
        "country": "country",
        "city": "capital",
        "continent": "continent",
        "views": "views",
        "last_updated": "last_updated"
    }
else:
    DB_TYPE = "sqlite"
    column_names ={
        "country": "Country/Territory",
        "city": "City/Town",
        "continent": "Continent",
        "views": "Views",
        "last_updated": "Last Updated"
    }