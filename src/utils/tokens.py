import os
import time
import uuid
import jwt


def create_access_token(client, user, application):
    headers = {
        "typ": 'at+jwt'
    }

    now = time.time()
    payload = {
        "iss": 'auth.rykroon.com', #use ENV var
        "aud": application.pk,
        "sub": user.pk,
        "exp": now + client.jwt_access_token_expires,
        "iat": now,
        "jti": str(uuid.uuid4())
    }

    return jwt.encode(payload=payload, key=client.secret, headers=headers)


def create_refresh_token(client, user, application):
    headers = {
        "typ": 'rt+jwt'
    }

    now = time.time()
    payload = {
        "iss": 'auth.rykroon.com', #use ENV var
        "aud": application.pk,
        "sub": user.pk,
        "exp": now + client.jwt_refresh_token_expires,
        "iat": now,
        "jti": str(uuid.uuid4())
    }

    return jwt.encode(payload=payload, key=client.secret, headers=headers)


def create_email_verification_token(client, user, email):
    headers = {
        "typ": 'email_verification'
    }

    now = time.time()
    payload = {
        "iss": 'auth.rykroon.com', #use ENV var
        #"aud": application.pk,
        "sub": user.pk,
        "exp": now + client.email_verification_expires,
        "iat": now,
        "jti": str(uuid.uuid4()),
        "email": email
    }

    return jwt.encode(payload=payload, key=client.secret, headers=headers)


def verify_access_token(token, client):
    headers = jwt.get_unverified_header(token)
    if headers.get('typ') != 'at+jwt':
        return False

    try:
        payload = jwt.decode(token, client.secret)
    except Exception:
        return False

    issuer = payload.get('iss')
    audience = payload.get('aud')


    if issuer != 'auth.rykroon.com':
        return False

    #check audience
    return True


def verify_refresh_token(token, client):
    headers = jwt.get_unverified_header(token)
    if headers.get('typ') != 'rt+jwt':
        return False

    try:
        payload = jwt.decode(token, client.secret)
    except Exception:
        return False

    issuer = payload.get('iss')
    audience = payload.get('aud')

    if issuer != 'auth.rykroon.com':
        return False

    #check audience
    return True