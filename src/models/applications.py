from mongoengine.fields import BooleanField, StringField, UUIDField
from .base import BaseDocument


APPLICATION_TYPES = ('NATIVE', 'WEB')


class Application(BaseDocument):
    name = StringField(required=True)
    description = StringField()
    type = StringField(choices=APPLICATION_TYPES)
    is_active = BooleanField(default=True)
    client_id = UUIDField(required=True)

    