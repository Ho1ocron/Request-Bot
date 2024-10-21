from sqlalchemy import text
from database_postgress import async_engine
from models import metadata_obj, Users


def insert_data():
    user = Users(username="1")