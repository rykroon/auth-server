from base64 import b64decode, b64encode
from functools import wraps
from hashlib import sha256
import hmac
import os
import time

from flask import request
from werkzeug.exceptions import BadRequest, Unauthorized

from models import Client
from utils import Cache


class BaseAuthentication:
    scheme = None

    def authenticate(self):
        authorization = request.headers.get('Authorization')
        if not authorization:
            raise BadRequest

        scheme, _, credentials = authorization.partition(' ')

        if scheme != self.scheme:
            return None

        return self.authenticate_credentials(credentials)

    def authenticate_credentials(self, credentials):
        raise NotImplementedError


class BasicAuthentication(BaseAuthentication):
    scheme = 'Basic'

    def authenticate_credentials(self, credentials):
        decoded_auth = b64decode(credentials)
        client_id, _, secret = decoded_auth.partition(':')
        
        client = Client.objects.filter(pk=client_id).first()
        if client is None:
            raise Unauthorized

        if client.secret != secret:
            raise Unauthorized

        return client


class HmacAuthentication(BaseAuthentication):
    scheme = 'HMAC'

    def authenticate_credentials(self, credentials):
        decoded_auth = b64decode(credentials)
        client_id, _, signature = decoded_auth.partition(':')

        client = Client.objects.filter(pk=client_id).first()
        if client is None:
            raise Unauthorized

        timestamp_header = os.getenv('HMAC_TIMESTAMP_HEADER', 'Timestamp')
        nonce_header = os.getenv('HMAC_NONCE_HEADER', 'Nonce')

        timestamp = request.headers.get(timestamp_header)
        nonce = request.headers.get(nonce_header)

        msg = "{method}{path}{payload}{timestamp}{nonce}".format(
            method=request.method,
            path=request.path,
            payload=request.data,
            timestamp=timestamp,
            nonce=nonce
        )

        digest = hmac.HMAC(
            key=client.secret.encode(),
            msg=msg.encode(),
            digestmod=sha256
        )

        calculated_signature = b64encode(digest).decode()

        if signature != calculated_signature:
            raise Unauthorized

        hmac_expires = int(os.getenv('HMAC_EXPIRES', 60 * 5))

        timestamp = float(timestamp)
        if time.time() - timestamp > hmac_expires:
            raise Unauthorized

        cache = Cache(key_prefix='nonce')
        if nonce in cache:
            raise Unauthorized

        cache.set(nonce, True, timeout=hmac_expires)

        return client

