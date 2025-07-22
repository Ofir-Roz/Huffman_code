"""
Application entry point using modern Flask patterns
"""

import os
from app import create_app
from config import config

def main() -> None:
    """Main application entry point"""
    # Get configuration from environment
    config_name = os.environ.get('FLASK_ENV', 'development')
    
    # Create application
    app = create_app()
    app.config.from_object(config.get(config_name, config['default']))
    
    # Initialize configuration
    config[config_name].init_app(app)
    
    # Run the application
    # Use 0.0.0.0 for production to allow external connections (required by Render)
    host = '0.0.0.0' if config_name == 'production' else os.environ.get('HOST', '127.0.0.1')
    port = int(os.environ.get('PORT', 5000))
    debug = config_name == 'development'
    
    app.run(host=host, port=port, debug=debug)


if __name__ == '__main__':
    main()
