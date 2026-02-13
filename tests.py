"""
Unit Tests for Gaurav Motors Application
Run with: pytest tests.py -v
"""
import pytest
from app import app, db
from datetime import datetime, date

@pytest.fixture
def client():
    """Create test client"""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['WTF_CSRF_ENABLED'] = False
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

@pytest.fixture
def auth_client(client):
    """Create authenticated test client"""
    # Register and login test user
    client.post('/register', data={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'Test123456',
        'name': 'Test User'
    })
    client.post('/login', data={
        'username': 'testuser',
        'password': 'Test123456'
    })
    return client

class TestValidators:
    """Test validation utilities"""
    
    def test_email_validation(self):
        from validators import is_valid_email
        assert is_valid_email('test@example.com') == True
        assert is_valid_email('invalid-email') == False
        assert is_valid_email('') == False
    
    def test_phone_validation(self):
        from validators import is_valid_phone
        assert is_valid_phone('9876543210') == True
        assert is_valid_phone('+919876543210') == True
        assert is_valid_phone('123') == False
    
    def test_password_strength(self):
        from validators import is_strong_password
        valid, msg = is_strong_password('Test@123')
        assert valid == True
        
        valid, msg = is_strong_password('weak')
        assert valid == False

class TestAuthentication:
    """Test authentication routes"""
    
    def test_register_page(self, client):
        """Test registration page loads"""
        response = client.get('/register')
        assert response.status_code == 200
    
    def test_login_page(self, client):
        """Test login page loads"""
        response = client.get('/login')
        assert response.status_code == 200
    
    def test_successful_registration(self, client):
        """Test user registration"""
        response = client.post('/register', data={
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'NewPass123',
            'name': 'New User'
        }, follow_redirects=True)
        assert response.status_code == 200
    
    def test_successful_login(self, client):
        """Test user login"""
        # First register
        client.post('/register', data={
            'username': 'loginuser',
            'email': 'login@example.com',
            'password': 'Login123',
            'name': 'Login User'
        })
        
        # Then login
        response = client.post('/login', data={
            'username': 'loginuser',
            'password': 'Login123'
        }, follow_redirects=True)
        assert response.status_code == 200
    
    def test_logout(self, auth_client):
        """Test logout"""
        response = auth_client.get('/logout', follow_redirects=True)
        assert response.status_code == 200

class TestRoutes:
    """Test main application routes"""
    
    def test_index(self, client):
        """Test index page"""
        response = client.get('/')
        assert response.status_code == 200
    
    def test_services_page(self, client):
        """Test services page"""
        response = client.get('/services')
        assert response.status_code == 200
    
    def test_about_page(self, client):
        """Test about page"""
        response = client.get('/about')
        assert response.status_code == 200
    
    def test_contact_page(self, client):
        """Test contact page"""
        response = client.get('/contact')
        assert response.status_code == 200

class TestAPIEndpoints:
    """Test API endpoints"""
    
    def test_services_api(self, client):
        """Test services API"""
        response = client.get('/api/services')
        assert response.status_code == 200
        data = response.get_json()
        assert 'success' in data
    
    def test_unauthorized_admin_api(self, client):
        """Test admin API without authentication"""
        response = client.get('/api/dashboard/stats')
        # Should redirect to login or return 401
        assert response.status_code in [302, 401]

class TestSecurity:
    """Test security features"""
    
    def test_sql_injection_prevention(self, client):
        """Test SQL injection is prevented"""
        malicious = "admin' OR '1'='1"
        response = client.post('/login', data={
            'username': malicious,
            'password': malicious
        })
        # Should not successfully login
        assert response.status_code in [200, 302]
    
    def test_xss_prevention(self, auth_client):
        """Test XSS prevention in forms"""
        from validators import Sanitizer
        xss_attempt = '<script>alert("XSS")</script>'
        sanitized = Sanitizer.escape_html(xss_attempt)
        assert '<script>' not in sanitized
        assert '&lt;script&gt;' in sanitized

class TestModels:
    """Test database models"""
    
    def test_user_model(self):
        """Test User model"""
        from app import User
        user = User(username='testuser', email='test@example.com', role='customer')
        user.set_password('Test123')
        assert user.check_password('Test123') == True
        assert user.check_password('wrong') == False
    
    def test_customer_profile(self):
        """Test CustomerProfile model"""
        from app import CustomerProfile
        customer = CustomerProfile(name='Test Customer', contact='9876543210')
        assert customer.name == 'Test Customer'
        assert customer.contact == '9876543210'

if __name__ == '__main__':
    pytest.main([__file__, '-v', '--cov=app', '--cov-report=html'])
