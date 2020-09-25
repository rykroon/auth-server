from datetime import datetime, timedelta
import os
from flask import jsonify
import jwt


JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
JWT_AUTHORIZATION_CODE_EXPIRES = int(os.getenv('JWT_AUTHORIZATION_CODE_EXPIRES'), 60) #defaults to 1 minute
JWT_ACCESS_TOKEN_EXPIRES = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 3600)) #defaults to 1 hour
JWT_REFRESH_TOKEN_EXPIRES = int(os.getenv('JWT_REFRESH_TOKEN_EXPIRES', 86400)) #defaults to 1 day


def create_access_token(sub, exp=None):
    if exp is None:
        exp = datetime.utcnow() + timedelta(seconds=JWT_ACCESS_TOKEN_EXPIRES)

    payload = dict(
        sub=sub,
        exp=exp,
        type='access'
    )

    return jwt.encode(payload=payload, key=JWT_SECRET_KEY)


def create_refresh_token(sub, exp=None, **kwargs):
    if exp is None:
        exp = datetime.utcnow() + timedelta(seconds=JWT_REFRESH_TOKEN_EXPIRES)

    payload = dict(
        sub=sub,
        exp=exp,
        type='refresh'
    )

    return jwt.encode(payload=payload, key=JWT_SECRET_KEY)


def get_access_token_response(access_token, token_type='bearer', expires_in=None, refresh_token=None):
    return jsonify(
        access_token=access_token,
        token_type=token_type,
        expires_in=JWT_ACCESS_TOKEN_EXPIRES,
        refresh_token=refresh_token
    )
