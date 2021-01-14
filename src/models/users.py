import crypt
from hashlib import sha256
import string
from mongoengine.errors import ValidationError
from mongoengine.fields import BooleanField, EmailField, StringField, UUIDField
from .base.fields import PhoneNumberField
from .base import BaseDocument


def mksalt():
    return crypt.mksalt(crypt.METHOD_SHA256)


def validate_username(username):
    valid_chars = string.ascii_letters + string.digits + '-_'
    if not all([char in valid_chars for char in username]):
        raise ValidationError('Username contains invalid characters.')

    if username[0] not in string.ascii_letters:
        raise ValidationError('Username must begin with a letter.')


class User(BaseDocument):
    username = StringField(max_length=150, validation=validate_username)

    first_name = StringField()
    last_name = StringField()
    
    email = EmailField()
    email_verified = BooleanField(default=False)

    phone_number = PhoneNumberField()
    phone_number_verified = BooleanField(default=False)

    salt = StringField(required=True, default=mksalt)
    password = StringField(required=True)

    is_active = BooleanField(default=True)

    client_id = UUIDField(required=True)

    @property
    def client(self):
        pass

    def set_password(self, password):
        salted_password = "{}{}".format(password, self.salt)
        self.password = sha256(salted_password.encode()).hexdigest()

    def check_password(self, password):
        salted_password = "{}{}".format(password, self.salt)
        hashed_password = sha256(salted_password.encode()).hexdigest()
        return self.password == hashed_password