import crypt
from hashlib import sha256
import re
import string
from mongoengine.errors import ValidationError
from mongoengine.fields import BooleanField, EmailField, StringField, UUIDField
from .mongoengineext import BaseDocument, PhoneNumberField


def mksalt():
    return crypt.mksalt(crypt.METHOD_SHA256)


def validate_username(username):
    valid_chars = string.ascii_letters + string.digits + '-_'
    if not all([char in valid_chars for char in username]):
        raise ValidationError('Username contains invalid characters.')

    if username[0] not in string.ascii_letters:
        raise ValidationError('Username must begin with a letter.')


class User(BaseDocument):
    first_name = StringField()
    last_name = StringField()
    username = StringField(max_length=150, validation=validate_username)

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

    def check_password(self, password):
        salted_password = "{}{}".format(password, self.salt)
        hashed_password = sha256(salted_password.encode()).hexdigest()
        return self.password == hashed_password

    def clean(self):
        super().clean()

        if self.pk is None:
            fields = list(self._fields.keys())
        else:
            fields = self._get_changed_fields()

        for field in fields:
            clean_method_name = '_clean_{}'.format(field)
            clean_method = getattr(self, clean_method_name, None)
            if clean_method:
                clean_method()

    def _clean_phone_number(self):
        """
            make sure the phone number begins with a "+" 
            and only contains digits
        """
        if self.phone_number is not None:
            self.phone_number = '+{}'.format(re.sub('[^0-9]', '', self.phone_number))

    def _clean_password(self):
        if self.password is not None:
            salted_password = "{}{}".format(self.password, self.salt)
            self.password = sha256(salted_password.encode()).hexdigest()
