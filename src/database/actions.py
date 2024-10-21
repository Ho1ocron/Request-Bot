import settings
from tortoise import Tortoise
from database.models import Task


async def init_db():
    await Tortoise.init(
        db_url='sqlite://db.sqlite3',
        modules={'models': settings.TORTOISE_MODELS},
    )
    await Tortoise.generate_schemas()


async def close_db():
    await Tortoise.close_connections()


async def create_user():
    await init_db()
    task = await Task.create(
	    name="First task",
	    description="First task description",
	)
    print(task)
    await close_db()
