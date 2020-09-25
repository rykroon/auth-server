from datetime import datetime, timedelta
import os
from flask import Blueprint, request, jsonify
from flask.views import MethodView
import jwt
import exceptions as exc
from tokens import create_access_token, create_refresh_token, get_access_token_response, get_error_response


oauth = Blueprint('oauth', __name__)


@oauth.route('/oauth/token', methods=['POST'])
class Token(MethodView):
    def post(self):
        payload = request.get_json()

        grant_type = payload.get('grant_type')

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
            payload = request.get_json()
            client_id = payload().get('client_id')
            client_secret = payload.get('client_secret')

        return jsonify(
            access_token=create_access_token(sub=client_id),
            token_type='bearer',
            expires_in='',
            refresh_token=''        
        )

    def refresh_token(self):
        payload = request.get_json()
        refresh_token = payload.get('refresh_token')
        jwt_secret_key = os.getenv('JWT_SECRET_KEY')
        jwt_payload = jwt.decode(refresh_token, key=jwt_secret_key)

        sub = jwt_payload.get('sub')
        return jsonify(
            access_token=create_access_token(sub=sub)
        )
