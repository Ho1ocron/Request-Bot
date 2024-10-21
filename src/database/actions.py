import settings
from typing import Optional
from tortoise import Tortoise
from database.models import User, Group


#------------------------------------------------------------Datavase config-----------------------------------------------------------#


async def init_db() -> None:
    await Tortoise.init(
        db_url='sqlite://db.sqlite3',
        modules={'models': settings.TORTOISE_MODELS},
    )
    await Tortoise.generate_schemas()


async def close_db() -> None:
    await Tortoise.close_connections()


#------------------------------------------------------------User database-----------------------------------------------------------#


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
        await user.save()
        print(user)
        return
    
    user = await User.get(id=user_id)
    user.name = username

    if group_id not in user.list_of_channels:
        user.list_of_channels.append(group_id)

    await user.save()
    print(user.id, user.name, user.list_of_channels)
    

#------------------------------------------------------------Group database-----------------------------------------------------------#


async def check_group_exists(group_id: int) -> bool:
    return await Group.filter(id=group_id).exists()


async def get_group(group_id: int) -> User:
    return await Group.get(id=group_id)


async def create_group(
        group_id: int,
        group_name: str,
        channel_name: str, 
        admin_list: list, 
        new_admin: Optional[int]
    ) -> None:
    
    exists = await check_group_exists(group_id=group_id)

    if not exists:
        group = await Group.create(
            id=group_id,
            name=group_name,
            channel_name=channel_name,
            admin_list=admin_list,
        )
        await group.save()
        return
    
    group = await Group.get(id=group_id)
    group.name = group_name
    group.channel_name = channel_name
    group.admin_list = admin_list

    await group.save()
    