from mongoengine.fields import StringField
from .base import BaseModel


class Application(BaseModel):
    name = StringField()
    description = StringField()
    client_id = ''

    