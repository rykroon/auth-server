from datetime import datetime, timedelta
import os
import uuid
from flask import jsonify
import jwt


JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
JWT_ACCESS_TOKEN_TTL = int(os.getenv('JWT_ACCESS_TOKEN_TTL', 3600)) #defaults to 1 hour
JWT_REFRESH_TOKEN_TTL = int(os.getenv('JWT_REFRESH_TOKEN_TTL', 86400)) #defaults to 1 day


#https://tools.ietf.org/html/rfc7519
#https://tools.ietf.org/html/draft-ietf-oauth-access-token-jwt-07


def create_access_token(sub, ttl=None):
    headers = {
        "typ": "at+jwt"
    }

    payload = {
        "sub": sub,
        "exp": datetime.utcnow() + timedelta(seconds=ttl or JWT_ACCESS_TOKEN_TTL),
        "iat": datetime.utcnow(),
        "jti": str(uuid.uuid4())
    }

    return jwt.encode(
        payload=payload, 
        key=JWT_SECRET_KEY, 
        headers=headers
    )


def create_refresh_token(sub, ttl=None):
    headers = {
        "typ": "rt+jwt"
    }

    payload = {
        "sub": sub,
        "exp": datetime.utcnow() + timedelta(seconds=ttl or JWT_REFRESH_TOKEN_TTL),
        "iat": datetime.utcnow(),
        "jti": str(uuid.uuid4())
    }

    return jwt.encode(
        payload=payload, 
        key=JWT_SECRET_KEY, 
        headers=headers
    )


def verify_access_token(token):
    headers = jwt.get_unverified_header(token)
    if headers.get('typ') != 'at+jwt':
        raise Exception

    return jwt.decode(token, key=JWT_SECRET_KEY)


def verify_refresh_token(token):
    headers = jwt.get_unverified_header(token)
    if headers.get('typ') != 'rt+jwt':
        raise Exception

    return jwt.decode(token, key=JWT_SECRET_KEY)

