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

    def __set__(self, instance, value):
        try:
            phone_number = phonenumbers.parse(value)
            value = phonenumbers.format_number(phone_number, PhoneNumberFormat.E164)

        except phonenumberutil.NumberParseException:
            pass

        super().__set__(instance, value)


    def validate(self, value):
        super().validate(value)

        try:
            phone_number = phonenumbers.parse(value)
        except phonenumberutil.NumberParseException:
            self.error(self.error_msg % value)

        if self.check_is_valid_number:
            if not phonenumbers.is_valid_number(phone_number):
                self.error(self.error_msg % value)

