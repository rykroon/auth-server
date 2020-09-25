from datetime import datetime, timedelta
import os
from flask import jsonify
import jwt


JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
#JWT_AUTHORIZATION_CODE_EXPIRES = int(os.getenv('JWT_AUTHORIZATION_CODE_TTL'), 60) #defaults to 1 minute
JWT_ACCESS_TOKEN_TTL = int(os.getenv('JWT_ACCESS_TOKEN_TTL', 3600)) #defaults to 1 hour
JWT_REFRESH_TOKEN_TTL = int(os.getenv('JWT_REFRESH_TOKEN_TTL', 86400)) #defaults to 1 day


def create_access_token(sub, ttl=None):
    if ttl is None:
        ttl = JWT_ACCESS_TOKEN_TTL
        
    exp = datetime.utcnow() + timedelta(seconds=ttl)
    return create_token(sub, exp, 'access')


def create_refresh_token(sub, ttl=None):
    if ttl is None:
        ttl = JWT_REFRESH_TOKEN_TTL
    
    exp = datetime.utcnow() + timedelta(seconds=ttl)
    return create_token(sub, exp, 'refresh')


def create_token(sub, exp, token_type):
    payload = dict(
        sub=sub,
        exp=exp,
        type=token_type
    )

    return jwt.encode(payload=payload, key=JWT_SECRET_KEY)


def decode_token(token):
    return jwt.decode(token, key=JWT_SECRET_KEY)


def get_access_token_response(access_token, token_type='bearer', expires_in=None, refresh_token=None):
    return jsonify(
        access_token=access_token,
        token_type=token_type,
        expires_in=JWT_ACCESS_TOKEN_TTL,
        refresh_token=refresh_token
    )
