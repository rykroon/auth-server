from random import randint
import secrets

from flask import current_app, jsonify, request
from flask.views import MethodView

from models import Client, User


class Login(MethodView):
    def post(self):
        client_id = request.json.get('client_id')
        client = Client.objects.filter(uuid=client_id).first()
        if not client:
            raise Exception

        auth_method = request.json.get('auth_method')

        if auth_method not in client.auth_methods:
            raise Exception

        if auth_method == 'password':
            self.password()

        if auth_method == 'email_link':
            self.email_link()

        if auth_method == 'phone_number':
            self.phone_number()

    def password(self):
        email = request.json.get('email')
        password = request.json.get('password')
        user = User.objects.filter(email=email).first()

        if not user:
            raise Exception

        if not user.email_verified:
            raise Exception

        if not user.check_password(password):
            raise Exception

        return True

    def email_link(self):
        email = request.json.get('email')
        user = User.objects.get(email=email)
        if not user:
            raise Exception

        if not user.email_verified:
            raise Exception

        token = secrets.token_urlsafe()
        #send email

    def phone_number(self):
        phone_number = request.json.get('phone_number')
        user = User.objects.get(phone_number=phone_number)
        if not user:
            raise Exception

        if not user.phone_number_verified:
            raise Exception

        otp = str(randint(0, 999999)).zfill(6)
        #send phone number

