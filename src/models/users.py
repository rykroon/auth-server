import crypt
from hashlib import sha256
from mongoengine.fields import BooleanField, EmailField, StringField
from .base import BaseModel


def mksalt():
    return crypt.mksalt(crypt.METHOD_SHA256)


class User(BaseModel):
    username = StringField()
    
    email = EmailField()
    email_verified = BooleanField(default=False)

    phone_number = StringField()
    phonenumber_verified = BooleanField(default=False)

    salt = StringField(required=True, default=mksalt)
    password = StringField(required=True)

    is_active = BooleanField(default=True)

    def set_password(self, password):
        salted_password = "{}{}".format(password, self.salt)
        self.password = sha256(salted_password.encode()).hexdigest()

    def check_password(self, password):
        salted_password = "{}{}".format(password, self.salt)
        hashed_password = sha256(salted_password.encode()).hexdigest()
        return self.password == hashed_password