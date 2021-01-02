from flask import jsonify, request
from werkzeug.exceptions import BadRequest, Conflict, Unauthorized
from models import Application, Client, User
from utils import create_access_token, create_refresh_token
from .base import BaseView


AUTH_METHOD_CHOICES = ('password', 'email_link', 'phone_number')
IDENTIFIER_TYPES = ('username', 'email', 'phone_number')


class TokenView(BaseView):

    def post(self):
        auth_method = self.get_param('auth_method', choices=AUTH_METHOD_CHOICES)

        application_id = request.json.get('application_id')
        self.application = Application.objects.get(pk=application_id)
        self.client = Client.objects.get(pk=self.application.client_id)

        if auth_method == 'password':
            self.password()

        elif auth_method == 'email_link':
            self.email_link()

        elif auth_method == 'phone_number':
            self.phone_number()

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

        self.user = self.get_document(User, identifier_type=identifier, client_id=self.client.pk)
        if not self.user.check_password(password):
            raise Unauthorized("Invalid {} or password".format(identifier_type))

    def email_link(self):
        email = self.get_param('email')
        self.user = self.get_document(User, email=email, client_id=self.client.pk)
        if not self.user.email_verified:
            raise Conflict("The email has not been verified.")

    def phone_number(self):
        phone_number = self.get_param('phone_number')
        self.user = self.get_document(User, phone_number=phone_number, client_id=self.client.pk)
        if not self.user.phone_number_verified:
            raise Conflict("The phone number has not been verified.")


