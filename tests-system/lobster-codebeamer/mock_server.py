from flask import Flask, jsonify
import logging

# Suppress Flask development server warning
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
# Config
CERT_PATH = 'tests-system/lobster-codebeamer/data/ssl/cert.pem'
KEY_PATH = 'tests-system/lobster-codebeamer/data/ssl/key.pem'
PORT = 5000
MOCK_ROUTE = '/api/v3/reports/1234/items'


def create_app():
    app = Flask(__name__)

    @app.route(MOCK_ROUTE, methods=['GET'])
    def mock_response():
        """Return mocked item response for Codebeamer integration."""
        return jsonify({
            "item": 5,
            "page": 1,
            "total": 1,
            "items": [
                {"item": {"id": 2, "version": 2, "tracker": {"id": 2}}}
            ]
        }), 200

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(
        host='0.0.0.0',
        port=PORT,
        ssl_context=(CERT_PATH, KEY_PATH)
    )
