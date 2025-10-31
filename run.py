#!/usr/bin/env python3
"""
Pet Management System - Application Entry Point
Run this file to start the Flask application
"""

from app import create_app
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create Flask application
app = create_app()

if __name__ == '__main__':
    # Get configuration from environment
    debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    host = os.getenv('FLASK_HOST', '127.0.0.1')
    port = int(os.getenv('FLASK_PORT', 5000))
    
    print("🐕 Pet Management System")
    print("=" * 40)
    print(f"Starting server on http://{host}:{port}")
    print("Debug mode:", debug)
    print("=" * 40)
    
    # Run the application
    app.run(
        host=host,
        port=port,
        debug=debug
    )
