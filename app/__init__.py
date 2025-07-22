"""
Flask application package
"""

from flask import Flask

from .routes import api_bp


def create_app() -> Flask:
    """
    Application factory pattern for creating Flask app.
    
    Returns:
        Configured Flask application
    """
    app = Flask(__name__)
    
    # Register blueprints
    app.register_blueprint(api_bp)
    
    return app
