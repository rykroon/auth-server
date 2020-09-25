from flask import jsonify


def oauth_error_handler(e):
    return jsonify(
        error=e.error,
        error_description=e.error_description
    ), e.status_code