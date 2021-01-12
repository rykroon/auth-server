from random import randint

from flask import jsonify, request
from werkzeug.exceptions import BadRequest, Conflict, Unauthorized

from models import Application, Client, User
from utils import create_access_token, create_refresh_token
from .base import BaseView


AUTH_METHOD_CHOICES = ('password', 'email', 'phone_number', 'refresh_token')
IDENTIFIER_TYPES = ('username', 'email', 'phone_number')


class TokenView(BaseView):

    def post(self):
        application_id = self.get_param('application_id')
        self.application = self.get_document(Application, pk=application_id, is_active=True)
        self.client = self.get_document(Client, pk=self.application.client_id)

        auth_method = self.get_param('auth_method', choices=AUTH_METHOD_CHOICES)

        if auth_method == 'password':
            self.password()

        elif auth_method == 'email':
            self.email()

        elif auth_method == 'phone_number':
            self.phone_number()

        elif auth_method == 'refresh_token':
            self.refresh_token()

        return jsonify(
            access_token=create_access_token(self.client, self.user, self.application),
            token_type='bearer',
            expires_in=self.client.jwt_access_token_expires,
            refresh_token=create_refresh_token(self.client, self.user, self.application)
        )

    def password(self):
        identifier_type = self.get_param('identifier_type', choices=IDENTIFIER_TYPES)
        identifier = self.get_param('identifier')
        password = self.get_param('password')

        filter_ = {
            identifier_type: identifier,
            'client_id': self.client.pk
        }

        self.user = self.get_document(User, **filter_)
        if not self.user.check_password(password):
            raise Unauthorized("Invalid {} or password".format(identifier_type))

    def email(self):
        email = self.get_param('email')
        self.user = self.get_document(User, email=email, client_id=self.client.pk)
        if not self.user.email_verified:
            raise Conflict("The email has not been verified.")

        otp = str(randint(0, 999999)).zfill(6)
        #send the one time password to the email

        #might use a different endpoint to send the OTPs, and then use this endpoint to verify

    def phone_number(self):
        phone_number = self.get_param('phone_number')
        self.user = self.get_document(User, phone_number=phone_number, client_id=self.client.pk)
        if not self.user.phone_number_verified:
            raise Conflict("The phone number has not been verified.")

        otp = str(randint(0, 999999)).zfill(6)

        #send one-time-password to phone-number

    def refresh_token(self):
        refresh_token = self.get_param('refresh_token')
        #verify the refresh token using self.client.secret as the key


