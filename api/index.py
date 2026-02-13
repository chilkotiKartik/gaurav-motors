"""
Vercel Serverless Entry Point for Gaurav Motors
Routes all requests through the Flask app
"""
import sys
import os

# Set VERCEL env var to trigger Vercel-specific config
os.environ['VERCEL'] = '1'

# Add parent directory to path so we can import app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import Flask app (this will verify DATABASE_URL is set)
try:
    from app import app
except RuntimeError as e:
    # Database configuration error - return error response
    from flask import Flask
    error_app = Flask(__name__)
    
    @error_app.route('/', defaults={'path': ''})
    @error_app.route('/<path:path>')
    def error_handler(path):
        return {
            'error': str(e),
            'message': 'Application configuration error. Check environment variables.'
        }, 500
    
    app = error_app

# Vercel expects the WSGI app object

