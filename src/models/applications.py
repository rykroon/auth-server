from mongoengine.fields import BooleanField, StringField, UUIDField
from .base import BaseDocument


class Application(BaseDocument):
    name = StringField(required=True)
    description = StringField()
    is_active = BooleanField(default=True)
    client_id = UUIDField(required=True)

    