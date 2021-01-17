import re
from flask import current_app
from mongoengine.fields import StringField
from mongoengine.errors import ValidationError
import phonenumbers
from phonenumbers import PhoneNumberFormat
from phonenumbers import phonenumberutil


class PhoneNumberField(StringField):
    error_msg = "Invalid phone number: %s"

    def __init__(self, check_is_valid_number=True, *args, **kwargs):
        self.check_is_valid_number = check_is_valid_number
        super().__init__(*args, **kwargs)

    def validate(self, value, clean=True):
        super().validate(value)

        if value is not None:
            try:
                phone_number = phonenumbers.parse(value)
            except phonenumberutil.NumberParseException:
                self.error(self.error_msg % value)

            if self.check_is_valid_number:
                if not phonenumbers.is_valid_number(phone_number):
                    self.error(self.error_msg % value)

