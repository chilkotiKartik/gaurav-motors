"""
Vercel Serverless Entry Point for Gaurav Motors
Routes all requests through the Flask app
"""
import sys
import os
import logging

# Set VERCEL env var to trigger Vercel-specific config
os.environ['VERCEL'] = '1'

# Add parent directory to path so we can import app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    from app import app
    
    # Check for DATABASE_URL in Vercel
    if not os.environ.get('DATABASE_URL'):
        logger.warning(
            "DATABASE_URL not set. App running with in-memory SQLite. "
            "Set DATABASE_URL environment variable to use persistent database."
        )
except Exception as e:
    logger.error(f"Failed to import app: {e}", exc_info=True)
    # Create error app if import fails
    from flask import Flask
    app = Flask(__name__)
    
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def error_handler(path):
        return f"<h1>Application Error</h1><p>{str(e)}</p><p>Check logs for details.</p>", 500

# Vercel expects the WSGI app object

