from flask import Blueprint, request, jsonify
from flask.views import MethodView
from models import Client, User

bp = Blueprint('oauth', __name__)


class Token(MethodView):
    def post(self):
        grant_type = request.json.get('grant_type')

        if grant_type == 'client_credentials':
            return self.client_credentials_grant()

        if grant_type == 'password':
            return self.password_grant()

        if grant_type == 'refresh_token':
            return self.refresh_token_grant()

        raise Exception

    def client_credentials_grant(self):
        client = self.verify_client()
        if client.is_public():
            raise Exception

        return jsonify(
            access_token='',
            token_type='bearer',
            expires_in='',
            refresh_token=''
        )

    def password_grant(self):
        client = self.verify_client()
        username = request.json.get('username')
        password = request.json.get('password')

        user = User.objects.filter(email=username).first()
        if user is None:
            raise Exception

        if not user.check_password(password):
            raise Exception

        if not user.email_verified:
            raise Exception

        return jsonify(
            access_token='',
            token_type='bearer',
            expires_in='',
            refresh_token=''
        )
    
    def refresh_token_grant(self):
        client = self.verify_client()
        refresh_token = request.json.get('refresh_token')
        #payload = verify_refresh_token(refresh_token)

        return jsonify(
            access_token='',
            token_type='bearer',
            expires_in=''
        )

    def verify_client(self):
        if request.authorization:
            client_id, client_secret = request.authorization
        else:
            client_id = request.json.get('client_id')
            client_secret = request.json.get('client_secret')

        client = Client.objects.filter(uuid=client_id).first()
        if client is None:
            raise Exception

        if not client.is_public():
            if client.secret != client_secret:
                raise Exception

        return client


