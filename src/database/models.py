from tortoise import Model
from tortoise.fields import (
    IntField, 
    CharField, 
)


class Task(Model):
    id = IntField(primary_key=True)
    name = CharField(max_length=256)
    description = CharField(max_length=500)

    class Meta:
        table = "tasks"
