from random import randint

from flask import Blueprint, g, jsonify, request
from werkzeug.exceptions import BadRequest, Conflict, Unauthorized

from models import Application, Client, User
from utils import create_access_token, create_refresh_token
from .base import BaseView


bp = Blueprint('tokens', __name__)

AUTH_METHOD_CHOICES = ('password', 'refresh_token')
IDENTIFIER_TYPES = ('username', 'email', 'phone_number')


class TokenView(BaseView):

    def post(self):
        application_id = self.get_param('application_id')
        self.application = Application.objects.filter(
            pk=application_id,
            is_active=True
        ).first_or_400(
            msg='Invalid application_id.'
        )

        self.client = Client.objects.filter(
            pk=self.application.client_id
        ).first_or_400(
            msg='Invalid client.'
        )

        auth_method = self.get_param('auth_method', choices=AUTH_METHOD_CHOICES)

        if auth_method == 'password':
            self.password()

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

        self.user = User.objects.filter(
            **filter_
        ).first()

        if self.user is None or not self.user.check_password(password)
            raise Unauthorized("Invalid {} or password".format(identifier_type))

    def refresh_token(self):
        refresh_token = self.get_param('refresh_token')
        #verify the refresh token using self.client.secret as the key


token_view = TokenView.as_view('TokeView')
bp.add_url_rule('/tokens', view_func=token_view, methods=['POST'])

