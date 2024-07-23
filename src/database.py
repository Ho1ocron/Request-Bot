from settings import (
    DB_HOST,
    DB_NAME,
    DB_PASS,
    DB_PORT,
    DB_USER,
)

from sqlalchemy import URL, create_engine, text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import Session, sessionmaker


# url = URL.create(
#     drivername="postgresql",
#     username="coderpad",
#     host="/tmp/postgresql/socket",
#     database="coderpad"
# )
# engine = create_engine(url)


engine = create_async_engine(f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

with engine.connect() as conn:
    res = conn.execute(text("Select vers"))
    print(f"{res=}")
