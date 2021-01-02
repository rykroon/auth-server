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
