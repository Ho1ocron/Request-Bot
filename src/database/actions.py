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


#------------------------------------------------------------Datavase config-----------------------------------------------------------#


async def init_db() -> None:
    if DEBUG:
        await Tortoise.init(
            db_url='sqlite://db.sqlite3',
            modules={'models': TORTOISE_MODELS},
        )
        await Tortoise.generate_schemas()
    else:
        await Tortoise.init(
            # postgres://myuser:mypassword@localhost:5432/mydb
            db_url=f"postgres://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
            modules={'models': TORTOISE_MODELS},
        )
        await Tortoise.generate_schemas()
    return


async def close_db() -> None:
    await Tortoise.close_connections()


#------------------------------------------------------------User database-------------------------------------------------------------#
async def get_users_groups(user_id: int) -> tuple[list[str], list[int]]:
    user = await User.get_or_none(user_id=user_id)
    if not user:
        return ([], [])
    await user.fetch_related("groups")  # load the ManyToMany relation
    return ([group.name for group in user.groups], [group.group_id for group in user.groups])


async def check_user_exists(user_id: int) -> bool:
    return await User.filter(id=user_id).exists()


async def get_user(user_id: int) -> User:
    return await User.get_or_none(user_id=user_id)


async def create_user(user_id: int, name: str, group_id: int) -> None:
    user = await User.get_or_none(user_id=user_id)
    group = await Group.get(group_id=group_id)

    if user:
        # Update username if changed
        if user.name != name:
            user.name = name
            await user.save()

        # Ensure membership exists
        membership = await GroupMembership.get_or_none(user=user, group=group)
        if not membership:
            await GroupMembership.create(user=user, group=group)
        return

    # Create new user
    user = await User.create(user_id=user_id, name=name)
    await GroupMembership.create(user=user, group=group)


#------------------------------------------------------------Group database-----------------------------------------------------------#


async def is_user_in_group(user_id: int, group_id: int) -> bool:
    user = await User.get_or_none(user_id=user_id)
    if not user:
        return False
    return await user.groups.filter(group_id=group_id).exists()


async def get_group(group_id: int) -> Group:
    return await Group.get(group_id=group_id)


async def delete_group(group_id: int) -> str:
    group = await Group.get_or_none(id=group_id)
    if group:
        group.delete()
    else:
        raise GroupNotFoundError(group_id=group_id)


async def create_group(group_id: int, name: str) -> None:
    group = await Group.filter(group_id=group_id).first()

    if group:
        if group.name != name:
            group.name = name
            await group.save()
    else:
        await Group.create(group_id=group_id, name=name)


async def ban_user(user_id: int, group_id: int, reason: str | None = None) -> None:
    user = await User.get_or_none(user_id=user_id)
    group = await Group.get_or_none(group_id=group_id)
    if not user or not group:
        return

    membership = await GroupMembership.get_or_none(user=user, group=group)
    if not membership:
        # Create record if not exists
        return
        # membership = await GroupMembership.create(user=user, group=group)

    membership.is_banned = True
    membership.banned_reason = reason
    membership.banned_at = datetime.now(timezone.utc)
    await membership.save()