from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException


def create_app():
    app = Flask(__name__)

    @app.errorhandler(HTTPException)
    def http_exception_handler(e):
        return jsonify(
            error=e.name,
            error_description=e.description
        ), e.code

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)


