import asyncio

from settings import (
    DB_HOST,
    DB_NAME,
    DB_PASS,
    DB_PORT,
    DB_USER,
    DEBUG,
)

from sqlalchemy import URL, create_engine, text, inspect
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import Session, sessionmaker, DeclarativeBase


url = URL.create(
    username=DB_USER,
    host=DB_HOST,
    port=DB_PORT,
    password=DB_PASS,
    drivername="postgresql+asyncpg",
    database=DB_NAME,
)

async_engine = create_async_engine(url=url, echo=True)

async_session = async_sessionmaker(async_engine)


class Base(DeclarativeBase):
    pass




async def async_main(url: URL) -> None:
    async with async_engine.connect() as conn:
        await conn.run_sync(Base.metadata.create_all)


asyncio.run(async_main(url=url))

#engine = create_async_engine(f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

# https://coderpad.io/blog/development/sqlalchemy-with-postgresql/

# https://github.com/mikemka/rcon-tg-bot/blob/master/handlers/event_group_message.py

