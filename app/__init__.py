"""
Flask application package
"""

from flask import Flask, jsonify
from typing import Dict, Tuple

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
    
    # Global error handlers
    @app.errorhandler(404)
    def not_found(error) -> Tuple[Dict[str, str], int]:
        """Handle 404 errors"""
        return {'error': 'Endpoint not found'}, 404

    @app.errorhandler(405)
    def method_not_allowed(error) -> Tuple[Dict[str, str], int]:
        """Handle 405 errors"""
        return {'error': 'Method not allowed'}, 405
    
    return app
