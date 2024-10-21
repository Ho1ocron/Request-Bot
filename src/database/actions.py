import settings
from tortoise import Tortoise
from database.models import User


async def init_db() -> None:
    await Tortoise.init(
        db_url='sqlite://db.sqlite3',
        modules={'models': settings.TORTOISE_MODELS},
    )
    await Tortoise.generate_schemas()


async def close_db() -> None:
    await Tortoise.close_connections()


async def check_user_exists(user_id: int) -> bool:
    return await User.filter(id=user_id).exists()


async def get_user(user_id: int) -> User:
    return await User.get(id=user_id)


async def create_user(user_id: int, username: str, group_id: int) -> None:
    exists = await check_user_exists(user_id=user_id)

    if not exists:
        user = await User.create(
            id=user_id,
            name=username,
            list_of_channels=[group_id]
        )
        user.save()
        print(user)
        return
    
    user = await get_user(user_id=user_id)
    user.name = username
    if group_id not in user.list_of_channels:
        user.list_of_channels.append(group_id)
    await user.save()

    print(user.id, user.name, user.list_of_channels)
    
