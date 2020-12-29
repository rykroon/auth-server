import secrets
from mongoengine.fields import StringField
from .base import BaseModel


def generate_secret():
    return secrets.token_urlsafe()


class Client(BaseModel):
    name = StringField(required=True)
    description = StringField(required=True)
    secret = StringField(default=generate_secret)