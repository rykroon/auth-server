import secrets
from mongoengine.fields import IntField, StringField
from .base import BaseDocument


def generate_secret():
    return secrets.token_urlsafe()

FIFTEEN_MINUTES = 60 * 15
TWENTY_FOUR_HOURS = 60 * 60 * 24
THIRTY_DAYS = 60 * 60 * 24 * 30


class Client(BaseDocument):
    name = StringField(required=True)
    description = StringField(required=True)
    secret = StringField(default=generate_secret)

    jwt_access_token_expires = IntField(default=FIFTEEN_MINUTES)
    jwt_refresh_token_expires = IntField(default=THIRTY_DAYS)
    email_verification_expires = IntField(default=TWENTY_FOUR_HOURS)
    