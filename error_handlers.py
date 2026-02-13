"""
Error Handlers and Custom Error Pages
Provides user-friendly error pages and proper error logging
"""
from flask import render_template, jsonify, request
import logging
from datetime import datetime

def init_error_handlers(app):
    """Initialize error handlers for the Flask app"""
    
    # Configure logging
    if not app.debug:
        # File handler for production errors
        file_handler = logging.FileHandler('error.log')
        file_handler.setLevel(logging.ERROR)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('Gaurav Motors startup')
    
    @app.errorhandler(400)
    def bad_request(error):
        """Handle 400 Bad Request"""
        if request.path.startswith('/api/'):
            return jsonify({'error': 'Bad Request', 'message': str(error)}), 400
        return render_template('errors/400.html', error=error), 400
    
    @app.errorhandler(401)
    def unauthorized(error):
        """Handle 401 Unauthorized"""
        if request.path.startswith('/api/'):
            return jsonify({'error': 'Unauthorized', 'message': 'Authentication required'}), 401
        return render_template('errors/401.html', error=error), 401
    
    @app.errorhandler(403)
    def forbidden(error):
        """Handle 403 Forbidden"""
        if request.path.startswith('/api/'):
            return jsonify({'error': 'Forbidden', 'message': 'Access denied'}), 403
        return render_template('errors/403.html', error=error), 403
    
    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 Not Found"""
        if request.path.startswith('/api/'):
            return jsonify({'error': 'Not Found', 'message': 'Resource not found'}), 404
        return render_template('errors/404.html', error=error), 404
    
    @app.errorhandler(405)
    def method_not_allowed(error):
        """Handle 405 Method Not Allowed"""
        if request.path.startswith('/api/'):
            return jsonify({'error': 'Method Not Allowed', 'message': str(error)}), 405
        return render_template('errors/405.html', error=error), 405
    
    @app.errorhandler(413)
    def request_entity_too_large(error):
        """Handle 413 File Too Large"""
        if request.path.startswith('/api/'):
            return jsonify({'error': 'File Too Large', 'message': 'File size exceeds 16MB limit'}), 413
        return render_template('errors/413.html', error=error), 413
    
    @app.errorhandler(500)
    def internal_server_error(error):
        """Handle 500 Internal Server Error"""
        app.logger.error(f'Server Error: {error}, URL: {request.url}')
        if request.path.startswith('/api/'):
            return jsonify({'error': 'Internal Server Error', 'message': 'An unexpected error occurred'}), 500
        return render_template('errors/500.html', error=error), 500
    
    @app.errorhandler(503)
    def service_unavailable(error):
        """Handle 503 Service Unavailable"""
        if request.path.startswith('/api/'):
            return jsonify({'error': 'Service Unavailable', 'message': 'Service temporarily unavailable'}), 503
        return render_template('errors/503.html', error=error), 503
    
    @app.before_request
    def log_request():
        """Log each request"""
        if app.debug:
            app.logger.debug(f'{request.method} {request.url}')
    
    @app.after_request
    def add_security_headers(response):
        """Add security headers to all responses"""
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        return response
    
    return app

def log_user_action(user_id, action, details=None):
    """Log user actions for audit trail"""
    log_entry = {
        'timestamp': datetime.utcnow().isoformat(),
        'user_id': user_id,
        'action': action,
        'details': details or {},
        'ip': request.remote_addr if request else None
    }
    logging.info(f"User Action: {log_entry}")
    return log_entry
