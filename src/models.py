from settings import DEBUG
from ast import literal_eval
from sqlalchemy import Table, Column, Integer, String, MetaData
from database import Base
from sqlalchemy.orm import Mapped, mapped_column


class Users(Base):
    __tablename__ = "users"
    username = Column(String, unique=True, index=True)
    user_id = Column(Integer, unique=True)


class Chats(Base):
    __tablename__ = "chats"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[int]
