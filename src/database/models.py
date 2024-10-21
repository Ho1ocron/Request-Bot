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


class Groups(Model):
    id = IntField(pk=True)
    name = CharField(max_length=255)
    admins = JSONField()

    def __str__(self):
        return super().__str__()
    class Meta:
        table = "groups"
    