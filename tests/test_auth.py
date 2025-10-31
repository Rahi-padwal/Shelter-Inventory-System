"""
Test cases for authentication functionality
"""

import pytest
from app import create_app, db
from app.models import User

@pytest.fixture
def app():
    """Create test application"""
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()

@pytest.fixture
def sample_user(app):
    """Create sample user for testing"""
    user = User(
        username='testuser',
        email='test@example.com',
        role='employee'
    )
    user.set_password('testpass123')
    
    with app.app_context():
        db.session.add(user)
        db.session.commit()
        yield user

def test_user_creation(app):
    """Test user creation and password hashing"""
    with app.app_context():
        user = User(
            username='newuser',
            email='newuser@example.com',
            role='employee'
        )
        user.set_password('password123')
        
        db.session.add(user)
        db.session.commit()
        
        # Verify user was created
        assert User.query.filter_by(username='newuser').first() is not None
        
        # Verify password hashing
        assert user.check_password('password123')
        assert not user.check_password('wrongpassword')

def test_user_roles(app):
    """Test user role functionality"""
    with app.app_context():
        admin_user = User(username='admin', email='admin@test.com', role='admin')
        employee_user = User(username='employee', email='emp@test.com', role='employee')
        
        admin_user.set_password('pass')
        employee_user.set_password('pass')
        
        assert admin_user.is_admin()
        assert not admin_user.is_employee()
        assert employee_user.is_employee()
        assert not employee_user.is_admin()

def test_login_page_loads(client):
    """Test that login page loads correctly"""
    response = client.get('/login')
    assert response.status_code == 200
    assert b'Pet Management System' in response.data

def test_register_page_loads(client):
    """Test that register page loads correctly"""
    response = client.get('/register')
    assert response.status_code == 200
    assert b'Create Account' in response.data

def test_valid_login(client, sample_user):
    """Test valid user login"""
    response = client.post('/login', data={
        'username': 'testuser',
        'password': 'testpass123'
    }, follow_redirects=True)
    
    # Should redirect to dashboard
    assert response.status_code == 200

def test_invalid_login(client):
    """Test invalid login credentials"""
    response = client.post('/login', data={
        'username': 'nonexistent',
        'password': 'wrongpass'
    })
    
    # Should stay on login page with error
    assert response.status_code == 200
    assert b'Invalid username or password' in response.data

def test_user_registration(client):
    """Test user registration"""
    response = client.post('/register', data={
        'username': 'newuser',
        'email': 'newuser@example.com',
        'password': 'password123',
        'confirm_password': 'password123',
        'role': 'employee'
    }, follow_redirects=True)
    
    # Should redirect to login page
    assert response.status_code == 200
    assert b'Registration successful' in response.data

def test_registration_validation(client):
    """Test registration form validation"""
    # Test with missing required fields
    response = client.post('/register', data={
        'username': '',
        'email': 'test@example.com',
        'password': 'pass',
        'confirm_password': 'pass',
        'role': 'employee'
    })
    
    assert response.status_code == 200
    assert b'Username must be at least 3 characters long' in response.data

def test_password_mismatch(client):
    """Test password confirmation validation"""
    response = client.post('/register', data={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'password123',
        'confirm_password': 'differentpass',
        'role': 'employee'
    })
    
    assert response.status_code == 200
    assert b'Passwords do not match' in response.data
