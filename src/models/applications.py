from mongoengine.fields import ObjectIdField, StringField
from .base import BaseDocument


class Application(BaseDocument):
    name = StringField(required=True)
    description = StringField()
    client_id = ObjectIdField()

    