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

from tortoise import Tortoise, fields, models, run_async


class Task(models.Model):
    id = fields.IntField(primary_key=True)
    name = fields.CharField(max_length=256)
    description = fields.CharField(max_length=500)
    date_created = fields.DatetimeField(auto_now_add=True)
    date_updated = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "tasks"


async def main():
    await Tortoise.init(
        db_url="sqlite://../databases/bot_db.db",
        # Модулем для моделей указываем __main__,
        # т.к. все модели для показа будем прописывать
        # именно тут
        modules={'models': ['__main__']},
    )
    await Tortoise.generate_schemas()

    task = await Task.create(
	    name="First task",
	    description="First task description"
	)
    print(task)
    # Output: <Task>
    print(task.name)
    # Output: First task

    task.name = "First task updated name"
    await task.save()
    print(task.name)
    # Output: First task updated name

    await Tortoise.close_connections()


if __name__ == "__main__":
    run_async(main())