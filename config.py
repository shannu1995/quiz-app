import os
basedir = os.path.abspath(os.path.dirname(__file__))
class Config(object):
    DB_PATH = os.getenv("DB_PATH")
    CAPITALS_TABLE_NAME = os.getenv("CAPITALS_TABLE_NAME")