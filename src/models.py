from datetime import datetime
import locale
import pytz
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
        self.date_created = datetime.utcnow()


CLIENT_TYPES = ('confidential', 'credentialed', 'public')
CLIENT_PROFILES = ('web application', 'browser-based application', 'native application')
CLIENT_TYPE_PROFILE_MAPPING = {
    'confidential': ('web application', ),
    'credentialed': ('web application', ),
    'public': ('browser-based application', 'native application')
}


class Client(BaseModel):
    type = StringField(required=True, choices=CLIENT_TYPES)
    profile = StringField(required=True, choices=CLIENT_PROFILES)
    secret = StringField()
    redirect_uri = ListField(field=URLField)

    def clean(self):
        super().clean()
        valid_profiles = CLIENT_TYPE_PROFILE_MAPPING.get(self.type, [])
        if self.profile not in valid_profiles:
            raise ValidationError("Invalid 'profile'")


class User(BaseModel):
    name = StringField()
    given_name = StringField()
    family_name = StringField()
    middle_name = StringField()
    nickname = StringField()
    preferred_username = StringField()
    profile = URLField()
    picture = URLField()
    website = URLField()
    email = EmailField()
    email_verified = BooleanField(default=False)
    gender = StringField(choices=('male', 'female'))
    birthdate = DateTimeField()
    zoneinfo = StringField(choices=pytz.all_timezones)
    locale = StringField(choices=list(locale.locale_alias.keys()))
    phone_number = StringField()
    phonenumber_verified = BooleanField(default=False)
    #address = 
    #updated_at = 