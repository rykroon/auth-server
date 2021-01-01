import os
import time
import uuid
import jwt


jwt_secret_key = os.getenv('JWT_SECRET_KEY')
jwt_access_token_expires = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 60 * 60)) #defaults to 1 hour
jwt_refresh_token_expires = int(os.getenv('JWT_REFRESH_TOKEN_EXPIRES', 60 * 60 * 24)) #defaults to 1 day


def create_token(typ='at+jwt', **kwargs):
    headers = {
        "typ": typ
    }
    now = time.time()
    payload = {
        "iss": 'auth.rykroon.com', #use ENV var
        "aud": '', # the application uuid
        "sub": '', # the user uuid
        "exp": now + jwt_access_token_expires,
        "iat": now,
        "jti": str(uuid.uuid4())
    }