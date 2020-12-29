from flask import Flask, g, jsonify
from utils import JSONEncoder, get_redis_client, error_handlers


def create_app():
    app = Flask(__name__)
    app.json_encoder = JSONEncoder

    for exc, handler in error_handlers.items():
        app.register_error_handler(exc, handler)

    @app.before_request
    def before_request():
        g.redis_client = get_redis_client()

    @app.route('/healthz', methods=['GET'])
    def health():
        return "OK"

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', debug=True)


