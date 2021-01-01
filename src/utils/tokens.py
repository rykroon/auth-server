import os
import time
import uuid
import jwt


#These global values should be able to be configured at the client level
jwt_secret_key = os.getenv('JWT_SECRET_KEY')
jwt_access_token_expires = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 60 * 15)) #defaults to 15 minutes
jwt_refresh_token_expires = int(os.getenv('JWT_REFRESH_TOKEN_EXPIRES', 60 * 60 * 24 * 30)) #defaults to 30 days


def create_token(user, application, typ='at+jwt', **kwargs):
    headers = {
        "typ": typ
    }
    now = time.time()
    payload = {
        "iss": 'auth.rykroon.com', #use ENV var
        "aud": application.pk,
        "sub": user.pk,
        "exp": now + jwt_access_token_expires,
        "iat": now,
        "jti": str(uuid.uuid4())
    }