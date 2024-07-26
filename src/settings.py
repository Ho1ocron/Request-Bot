from ast import literal_eval
from pathlib import Path
from os import getenv
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent

DOTENV_PATH = BASE_DIR / '.env'

if DOTENV_PATH.exists():
    load_dotenv(DOTENV_PATH)

# * Telegram Config

TOKEN = getenv('TOKEN')

ADMIN_IDS = literal_eval(getenv('ADMIN_IDS'))

# * Database Config

DB_HOST = getenv('DB_HOST')

DB_PORT = getenv('DB_PORT')

DB_USER = getenv('DB_USER')

DB_PASS = getenv('DB_PASS')

DB_NAME = getenv('DB_NAME')

DEBUG = getenv('DEBUG')


