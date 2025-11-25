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

DB_URL = getenv('DB_URL')

DEBUG = literal_eval(getenv('DEBUG'))

TORTOISE_MODELS = ['database.models']

if DEBUG:
    DATABASE_URL = "sqlite://db.sqlite3"
else:
    DATABASE_URL = f"postgres://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# * Redis Database Config

REDIS_DB_HOST = getenv('REDIS_DB_HOST')
REDIS_DB_USER = getenv('REDIS_DB_USER')
REDIS_DB_PASS = getenv('REDIS_DB_PASS')
REDIS_DB_NAME = getenv('REDIS_DB_NAME')
REDIS_DB_PORT = getenv('REDIS_DB_PORT')
REDIS_DEBUG = literal_eval(getenv('REDIS_DEBUG'))


DATABASE_CONFIG = {
    'connections': {
        'default': DATABASE_URL,
    },
    'apps': {
        'models': {
            'models': [
                'src.database.models',
                'aerich.models',
            ],
            'default_connection': 'default',
        },
    },
}