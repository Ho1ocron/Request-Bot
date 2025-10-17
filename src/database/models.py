from tortoise import Model
from tortoise.fields import (
    IntField, 
    CharField, 
    ManyToManyRelation,
    ManyToManyField, 
    BigIntField,
    BooleanField,
    ForeignKeyField,
    DatetimeField
)


class User(Model):
    id = IntField(pk=True)
    user_id = BigIntField(unique=True)
    name = CharField(max_length=50, unique=True)
    is_global_banned = BooleanField(default=False)

    groups: ManyToManyRelation["Group"] = ManyToManyField(
        "models.Group", related_name="users", through="group_membership"
    )
    
    class Meta:
        table = "users"

    def __str__(self):
        return f"User(id={self.id}, name={self.name})"


class Group(Model):
    id = IntField(pk=True)
    group_id = BigIntField(unique=True)
    name = CharField(max_length=100)

    users: ManyToManyRelation["User"]

    class Meta:
        table = "groups" 

    def __str__(self):
        return f"Group(id={self.id}, name={self.name})"


class GroupMembership(Model):
    """
    Intermediate table between User and Group.
    Stores ban info and timestamps per group.
    """
    id = IntField(pk=True)
    user = ForeignKeyField("models.User", related_name="group_memberships")
    group = ForeignKeyField("models.Group", related_name="group_memberships")

    is_banned = BooleanField(default=False)
    banned_reason = CharField(max_length=255, null=True)
    banned_at = DatetimeField(null=True)

    class Meta:
        table = "group_membership"
        unique_together = ("user", "group")


class GroupNotFoundError(Exception):
    def __init__(self, group_id: int | str) -> None:
        super().__init__(f"Group with ID {group_id} not found.")
        self.group_id = group_id


class UserNotFoundError(Exception):
    def __init__(self, user_id: int | str):
        super().__init__(f"User with ID {user_id} not found.")
        self.user_id = user_id