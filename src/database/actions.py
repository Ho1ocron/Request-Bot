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


    @classmethod
    async def create_user(cls, user_id: int, name: str, group_id: int) -> None:
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

    @classmethod
    async def get_user(cls, user_id: int) -> User:
        return await User.get_or_none(user_id=user_id)
    
    @classmethod
    async def get_users_groups(cls, user_id: int) -> tuple[list[str], list[int]]:
        user = await User.get_or_none(user_id=user_id)
        if not user:
            return ([], [])
        try:
            await user.fetch_related("group_membership")  # load the ManyToMany relation
        except Exception as e:
            print(e)
            return ([], [])
        return ([group.name for group in user.groups], [group.group_id for group in user.groups])
    
    #------------------------------------------------------------Group database-----------------------------------------------------------#
    @classmethod
    async def create_group(cls, group_id: int, name: str) -> None:
        group = await Group.filter(group_id=group_id).first()
        if group:
            if group.name != name:
                group.name = name
                await group.save()
        else:
            await Group.create(group_id=group_id, name=name)


    

