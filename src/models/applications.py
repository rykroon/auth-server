from mongoengine.fields import StringField, UUIDField
from .base import BaseDocument


class Application(BaseDocument):
    name = StringField(required=True)
    description = StringField()
    client_id = UUIDField(required=True)

    