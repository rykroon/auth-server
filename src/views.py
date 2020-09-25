from datetime import datetime, timedelta
import os
from flask import Blueprint, request, jsonify
from flask.views import MethodView
import jwt
import exceptions as exc
from tokens import create_access_token, create_refresh_token, decode_token


oauth = Blueprint('oauth', __name__)


@oauth.route('/oauth/token', methods=['POST'])
class Token(MethodView):
    def post(self):
        grant_type = request.json.get('grant_type')

        if grant_type == 'authorization_code':
            pass

        if grant_type == 'client_credentials':
            return self.client_credentials()

        if grant_type == 'refresh_token':
            return self.refresh_token()

        raise exc.UnsupportedGrantType

    def authorization_code(self):
        pass

    def client_credentials(self):
        if request.authorization:
            client_id, client_secret = request.authorization

        else:
            client_id = request.json.get('client_id')
            client_secret = request.json.get('client_secret')

        return jsonify(
            access_token=create_access_token(sub=client_id),
            token_type='bearer',
            expires_in='',
            refresh_token=''        
        )

    def refresh_token(self):
        refresh_token = request.json.get('refresh_token')
        jwt_payload = decode_token(refresh_token)

        if jwt_payload.get('type') != 'refresh':
            raise exc.InvalidGrant('Invalid token.')

        sub = jwt_payload.get('sub')
        return jsonify(
            access_token=create_access_token(sub=sub),
            token_type='bearer',
            expires_in=''
        )
