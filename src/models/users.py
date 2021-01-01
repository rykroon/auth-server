import crypt
from hashlib import sha256
from mongoengine.fields import BooleanField, EmailField, ObjectIdField, StringField
from .base.fields import PhoneNumberField
from .base import BaseDocument


def mksalt():
    return crypt.mksalt(crypt.METHOD_SHA256)


class User(BaseDocument):
    username = StringField()

    first_name = StringField()
    last_name = StringField()
    
    email = EmailField()
    email_verified = BooleanField(default=False)

    phone_number = PhoneNumberField()
    phone_number_verified = BooleanField(default=False)

    salt = StringField(required=True, default=mksalt)
    password = StringField(required=True)

    is_active = BooleanField(default=True)

    client_id = ObjectIdField()

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