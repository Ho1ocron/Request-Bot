from tortoise import Model
from tortoise.fields import (
    IntField, 
    CharField, 
    ManyToManyRelation,
    ManyToManyField, 
    BigIntField,
)


class User(Model):
    id = IntField(pk=True)
    user_id = BigIntField(unique=True)
    username = CharField(max_length=50, unique=True)

    groups: ManyToManyRelation["Group"] = ManyToManyField(
        "models.Group", related_name="users"
    )
    
    class Meta:
        table = "users"

    def __str__(self):
        return f"User(id={self.id}, username={self.username})"


class Group(Model):
    id = IntField(pk=True)
    group_id = BigIntField(unique=True)
    name = CharField(max_length=100)

    users: ManyToManyRelation["User"]

    class Meta:
        table = "groups" 

    def __str__(self):
        return f"Group(id={self.id}, name={self.name})"
    

class GroupNotFoundError(Exception):
    def __init__(self, group_id: int | str) -> None:
        super().__init__(f"Group with ID {group_id} not found.")
        self.group_id = group_id


class UserNotFoundError(Exception):
    def __init__(self, user_id: int | str):
        super().__init__(f"User with ID {user_id} not found.")
        self.user_id = user_id