import secrets
from mongoengine.fields import StringField
from .base import BaseDocument


def generate_secret():
    return secrets.token_urlsafe()


class Client(BaseDocument):
    name = StringField(required=True)
    description = StringField(required=True)
    secret = StringField(default=generate_secret)