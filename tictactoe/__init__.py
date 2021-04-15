"""Flask application factory."""
import os
import secrets
from flask import Flask


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.update(
        SECRET_KEY=os.environ.get("SECRET_KEY") or secrets.token_hex(32),
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
        MAX_CONTENT_LENGTH=4096,
    )
    if test_config:
        app.config.update(test_config)
    from .routes import bp
    app.register_blueprint(bp)
    return app
