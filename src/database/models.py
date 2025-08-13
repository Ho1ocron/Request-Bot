from tortoise import Model
from tortoise.fields import (
    IntField, 
    CharField, 
    JSONField, # Rewrite to relation
    BigIntField,
    ManyToManyField,
    ManyToManyRelation,
    BooleanField
)
class Channel(Model):
    id = BigIntField(pk=True)
    group_id = BigIntField()


class User(Model):
    id = BigIntField(pk=True) #id  в бд
    tg_id = BigIntField(unique=True)
    is_admin = BooleanField(default=False)
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
    admin_list: ManyToManyRelation[User] = ManyToManyField("models.User", related_name="admin_list")

    def __str__(self):
        return super().__str__()
    
    class Meta:
        table = "groups"
