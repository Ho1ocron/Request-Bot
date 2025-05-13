from settings import TORTOISE_MODELS, DEBUG
from typing import Optional
from tortoise import Tortoise
from tortoise.expressions import Q
from database.models import User, Group, GroupNotFoundError
from typing import Optional


#------------------------------------------------------------Datavase config-----------------------------------------------------------#


async def init_db() -> None:
    if DEBUG:
        await Tortoise.init(
            db_url='sqlite://db.sqlite3',
            modules={'models': TORTOISE_MODELS},
        )
        await Tortoise.generate_schemas()
    return

async def close_db() -> None:
    await Tortoise.close_connections()


#------------------------------------------------------------User database-------------------------------------------------------------#
async def get_users_groups(user_id: int) -> list[str]:
    user = await User.get_or_none(id=user_id)
    if not user or not user.list_of_channels:
        return []  # Return empty list if user doesn't exist or has no groups
    
    # Fetch group names based on stored group IDs
    groups = await Group.filter(id__in=user.list_of_channels).values_list("name", flat=True)
    
    return groups


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
        return
    
    user = await User.get(id=user_id)
    user.name = username

    if group_id not in user.list_of_channels:
        user.list_of_channels.append(group_id)

    await user.save()
    

#------------------------------------------------------------Group database-----------------------------------------------------------#


async def if_user_in_group(user_id: int, group_id: int) -> bool:
    group = await Group.get(id=group_id)
    user = await User.get_or_none(id=user_id)
    if user in group: return True
    return False


async def check_group_exists(group_id: int) -> bool:
    return await Group.filter(id=group_id).exists()


async def get_group(group_id: int) -> Group:
    return await Group.get(id=group_id)


async def delete_group(group_id: int) -> str:
    group = await Group.get_or_none(id=group_id)
    if group:
        group.delete()
    else:
        raise GroupNotFoundError(group_id=group_id)

async def create_group(
        group_id: int,
        group_name: str,
        admin_list: list, 
    ) -> None:
    
    exists = await check_group_exists(group_id=group_id)

    if not exists:
        group = await Group.create(
            id=group_id,
            name=group_name,
            admin_list=admin_list,
        )
        await group.save()
        return
    
    group = await Group.get(id=group_id)
    group.name = group_name
    group.admin_list += admin_list

    await group.save()

