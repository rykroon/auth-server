from flask import jsonify, request
from flask.views import MethodView
from tokens import create_access_token, create_refresh_token, verify_refresh_token



class Token(MethodView):
    def post(self):
        grant_type = request.json.get('grant_type')

        if grant_type == 'authorization_code':
            pass

        if grant_type == 'client_credentials':
            return self.client_credentials()

        if grant_type == 'password':
            return self.password()

        if grant_type == 'refresh_token':
            return self.refresh_token()

        raise Exception

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

    def password(self):
        client_id = request.json.get('client_id')
        username = request.json.get('username')
        password = request.json.get('password')

    def refresh_token(self):
        refresh_token = request.json.get('refresh_token')
        jwt_payload = verify_refresh_token(refresh_token)

        if jwt_payload.get('type') != 'refresh':
            raise exc.InvalidGrant('Invalid token.')

        sub = jwt_payload.get('sub')
        return jsonify(
            access_token=create_access_token(sub=sub),
            token_type='bearer',
            expires_in=''
        )