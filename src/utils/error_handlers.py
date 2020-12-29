
from flask import jsonify
from werkzeug.exceptions import HTTPException, Unauthorized, TooManyRequests


def handle_http_exception(e):
    return jsonify(
        error=e.name,
        error_description=e.description
    ), e.code


def handle_too_many_requests(e):
    resp = jsonify(
        error=e.name,
        error_description=e.description
    )
    resp.headers.add('Retry-After', e.retry_after)
    return resp, e.code


def handle_unauthorized(e):
    resp = jsonify(
        error=e.name,
        error_description=e.description
    )
    resp.headers.add('WWW-Authenticate', e.www_authenticate)
    return resp, e.code


error_handlers = {
    HTTPException: handle_http_exception,
    TooManyRequests: handle_too_many_requests,
    Unauthorized: handle_unauthorized
}