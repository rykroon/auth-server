from mongoengine.fields import StringField
from .base import BaseModel


class Client(BaseModel):
    name = StringField(required=True)
    description = StringField(required=True)
    secret = StringField()