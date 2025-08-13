from tortoise import Model
from tortoise.fields import (
    IntField, 
    CharField, 
    JSONField, # Rewrite to relation
    BigIntField,
    ManyToManyField,
    ManyToManyRelation
)
class Channel(Model):
    id = BigIntField(pk=True)
    group_id = BigIntField()


class User(Model):
    id = BigIntField(pk=True) #id  в бд
    tg_id = BigIntField(unique=True)
    name = CharField(max_length=256)
    # list_of_channels = ()
    channels_list: ManyToManyRelation[Channel] = ManyToManyField("models.Channel", related_name="channels_list")
    
    def __str__(self):
        return super().__str__()
    
    class Meta:
        table = "users"


class Group(Model):
    id = BigIntField(pk=True)
    group_id = BigIntField()
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