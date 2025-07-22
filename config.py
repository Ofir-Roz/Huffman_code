"""
Configuration settings for the Huffman coding application
"""

import os
from typing import Dict, Any


class Config:
    """Base configuration class"""
    
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = False
    TESTING = False
    
    # Application settings
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    JSON_AS_ASCII = False
    
    @staticmethod
    def init_app(app) -> None:
        """Initialize application with this config"""
        pass


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    
    @classmethod
    def init_app(cls, app) -> None:
        Config.init_app(app)
        # Development-specific initialization


class ProductionConfig(Config):
    """Production configuration"""
    
    @classmethod
    def init_app(cls, app) -> None:
        Config.init_app(app)
        
        # Production-specific initialization
        import logging
        import os
        
        if not app.debug and not app.testing:
            # For cloud platforms like Render, use console logging instead of file logging
            # since the filesystem is often read-only
            
            # Set up console logging with proper formatting
            import sys
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(logging.Formatter(
                '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
            ))
            console_handler.setLevel(logging.INFO)
            app.logger.addHandler(console_handler)
            
            app.logger.setLevel(logging.INFO)
            app.logger.info('Huffman Coding app startup - Production mode')


class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    WTF_CSRF_ENABLED = False


config: Dict[str, Config] = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
