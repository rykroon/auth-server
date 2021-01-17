import secrets
from mongoengine.fields import IntField, StringField
from .mongoengineext import BaseDocument


def generate_secret():
    return secrets.token_urlsafe()

FIFTEEN_MINUTES = 60 * 15
THIRTY_DAYS = 60 * 60 * 24 * 30


class Client(BaseDocument):
    name = StringField(required=True)
    description = StringField(required=True)
    secret = StringField(default=generate_secret)

    jwt_access_token_expires = IntField(default=FIFTEEN_MINUTES)
    jwt_refresh_token_expires = IntField(default=THIRTY_DAYS)
    