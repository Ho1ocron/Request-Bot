from ast import literal_eval
from pathlib import Path
from os import getenv
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent

DOTENV_PATH = BASE_DIR / '.env'

if DOTENV_PATH.exists():
    load_dotenv(DOTENV_PATH)

TOKEN = getenv('TOKEN')

ADMIN_IDS = literal_eval(getenv('ADMIN_IDS'))