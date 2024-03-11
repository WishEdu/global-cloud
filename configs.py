from os import environ
from pathlib import Path

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

ASSETS_DIR = Path(environ.get('ASSETS_DIR'))
DB_USER = environ.get('DB_USER')
DB_PASSWORD = environ.get('DB_PASSWORD')
DB_NAME = environ.get('DB_NAME')
PORT = 8006
MAIN_ROUTE = '/api'