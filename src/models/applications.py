from mongoengine.fields import BooleanField, ObjectIdField, StringField, UUIDField
from .mongoengineext import BaseDocument


APPLICATION_TYPES = ('NATIVE', 'WEB')


class Application(BaseDocument):
    client_id = ObjectIdField(required=True)
    name = StringField(required=True)
    description = StringField()
    type = StringField(choices=APPLICATION_TYPES)
    is_active = BooleanField(default=True)

    