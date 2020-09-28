from urllib.parse import quote, urlencode
from flask import jsonify, redirect


def token_error_handler(e):
    return jsonify(e.to_dict()), e.status_code


def authorization_error_handler(e):
    location = "{}?{}".format(e.redirect_uri, urlencode(e.to_dict(), quote_via=quote))
    return redirect(
        location=location
    )