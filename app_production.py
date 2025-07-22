#!/usr/bin/env python3
"""
Production startup script for Render deployment
"""

import os
from app import create_app

# Create the application with production config
app = create_app()

# Set production configuration
app.config.update(
    DEBUG=False,
    TESTING=False,
    SECRET_KEY=os.environ.get('SECRET_KEY', 'prod-secret-key-change-me'),
    JSON_AS_ASCII=False
)

if __name__ == '__main__':
    # Get port from environment (Render sets this)
    port = int(os.environ.get('PORT', 5000))
    
    # Run the app (bind to all interfaces for cloud deployment)
    app.run(host='0.0.0.0', port=port, debug=False)
