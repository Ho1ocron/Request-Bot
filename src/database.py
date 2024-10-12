import asyncio

from settings import (
    DB_HOST,
    DB_NAME,
    DB_PASS,
    DB_PORT,
    DB_USER,
    DEBUG,
)

#db path for now: ../databases/bot_db.db

from tortoise import Tortoise, fields, Model, run_async


class User(Model):
    id = fields.IntField(pk=True)
    chat_id = fields.BigIntField(unique=True)


    class Meta:
        table = "users"


async def main():
    await Tortoise.init(
        db_url='../databases/bot_db.db',  # Change to your database URL
        modules={'models': ['models']}
    )
    await Tortoise.generate_schemas()


if __name__ == "__main__":
    run_async(main())