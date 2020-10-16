import crypt
from datetime import datetime
from hashlib import sha256
import locale
import pytz
import secrets
import uuid
from mongoengine import Document
from mongoengine.errors import ValidationError
from mongoengine.fields import BooleanField, DateTimeField, EmailField, ListField, StringField, URLField, UUIDField


class BaseModel(Document):
    meta = {
        'abstract': True
    }

    uuid = UUIDField(required=True, default=uuid.uuid4, unique=True)
    date_created = DateTimeField(required=True, default=datetime.utcnow)
    date_updated = DateTimeField(required=True)

    def clean(self):
        self.date_updated = datetime.utcnow()


PASSWORD_AUTHENTICATION = 'password-authentication'
EMAIL_LINK_AUTHENTICATION = 'email-link-authentication'
GOOGLE_SIGN_IN = 'google-sign-in'
FACEBOOK_LOGIN = 'facebook-login'
PHONE_NUMBER = 'phone-number'

AUTHENTICATION_METHODS = (
    PASSWORD_AUTHENTICATION, 
    EMAIL_LINK_AUTHENTICATION,
    GOOGLE_SIGN_IN,
    FACEBOOK_LOGIN,
    PHONE_NUMBER
)


class Client(BaseModel):
    name = StringField(required=True)
    description = StringField(required=True)
    secret = StringField()
    authentication_methods = ListField(field=StringField)


def mksalt():
    return crypt.mksalt(crypt.METHOD_SHA256)


class User(BaseModel):
    salt = StringField(required=True, default=mksalt)
    password = StringField(required=True)

    name = StringField()
    given_name = StringField()
    family_name = StringField()
    middle_name = StringField()
    nickname = StringField()
    preferred_username = StringField()
    profile = URLField()
    picture = URLField()
    website = URLField()
    gender = StringField(choices=('male', 'female'))
    birthdate = DateTimeField()
    zoneinfo = StringField(choices=pytz.all_timezones)
    locale = StringField(choices=list(locale.locale_alias.keys()))
    #updated_at = 
    
    email = EmailField()
    email_verified = BooleanField(default=False)

    phone_number = StringField()
    phonenumber_verified = BooleanField(default=False)

    #address = 


    def set_password(self, password):
        salted_password = "{}{}".format(password, self.salt)
        self.password = sha256(salted_password.encode()).hexdigest()

    def check_password(self, password):
        salted_password = "{}{}".format(password, self.salt)
        hashed_password = sha256(salted_password.encode()).hexdigest()
        return self.password == hashed_password