#!/usr/bin/env python3
"""
Production startup script for Render deployment
"""

import os
from app import create_app

# Create the application
app = create_app()

if __name__ == '__main__':
    # Get port from environment (Render sets this)
    port = int(os.environ.get('PORT', 5000))
    
    # Run the app
    app.run(host='0.0.0.0', port=port)
