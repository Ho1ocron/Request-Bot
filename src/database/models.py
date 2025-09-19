from tortoise import Model
from tortoise.fields import (
    IntField, 
    CharField, 
    JSONField,
)


class User(Model):
    id = IntField(pk=True)
    name = CharField(max_length=256)
    list_of_channels = JSONField()
    
    def __str__(self):
        return super().__str__()
    
    class Meta:
        table = "users"


class Group(Model):
    id = IntField(pk=True)
    name = CharField(max_length=255)
    admin_list = JSONField()

    def __str__(self):
        return super().__str__()
    
    class Meta:
        table = "groups"


class GroupNotFoundError(Exception):
    def __init__(self, group_id: int | str) -> None:
        super().__init__(f"Group with ID {group_id} not found.")
        self.group_id = group_id


class UserNotFoundError(Exception):
    def __init__(self, user_id: int | str):
        super().__init__(f"User with ID {user_id} not found.")
        self.user_id = user_id