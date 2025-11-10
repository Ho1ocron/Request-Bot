from tortoise import Tortoise
from tortoise.expressions import Q

from datetime import datetime, timezone

from database.models import User, Group, GroupMembership, GroupNotFoundError
from settings import (
    TORTOISE_MODELS,
    DB_HOST,
    DB_NAME,
    DB_PASS,
    DB_PORT,
    DB_USER,
    DEBUG,
)


class DatabaseActions:
    @classmethod
    async def init_db(cls) -> None:
        db_url = (
            "sqlite://db.sqlite3"
            if DEBUG
            else f"postgres://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        )
        await Tortoise.init(
            db_url=db_url,
            modules={'models': TORTOISE_MODELS},
        )

        if DEBUG:
            await Tortoise.generate_schemas()

    @classmethod
    async def drop_db(cls) -> None:
        await Tortoise.close_connections()


    
    

