from flask import Flask
from error_handlers import oauth_error_handler
from exceptions import OAuthError


def create_app():
    app = Flask(__name__)
    app.register_error_handler(OAuthError, oauth_error_handler)
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)


