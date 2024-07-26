from settings import DEBUG
from ast import literal_eval
from sqlalchemy import Table, Column, Integer, String, MetaData
from database import Base
from sqlalchemy.orm import Mapped, mapped_column


class Users(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]


metadata_obj = MetaData()

users_table = Table(
    "users", 
    metadata_obj, 
    Column("id", Integer, primary_key=True),
    Column("username", String),
)


