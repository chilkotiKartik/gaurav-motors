"""
Vercel Serverless Entry Point for Gaurav Motors
Routes all requests through the Flask app
"""
import sys
import os

# Add parent directory to path so we can import app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set VERCEL env var to trigger Vercel-specific config
os.environ['VERCEL'] = '1'

from app import app

# Vercel expects the WSGI app object
app = app
