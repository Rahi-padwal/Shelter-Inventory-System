"""
Test cases for role-based permissions
"""

import pytest
from app import create_app, db
from app.models import User, Pet, Donation

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
def admin_user(app):
    """Create admin user"""
    user = User(username='admin', email='admin@test.com', role='admin')
    user.set_password('password123')
    
    with app.app_context():
        db.session.add(user)
        db.session.commit()
        yield user

@pytest.fixture
def employee_user(app):
    """Create employee user"""
    user = User(username='employee', email='emp@test.com', role='employee')
    user.set_password('password123')
    
    with app.app_context():
        db.session.add(user)
        db.session.commit()
        yield user

@pytest.fixture
def sample_pet(app):
    """Create sample pet"""
    pet = Pet(
        pet_name='Test Pet',
        breed='Test Breed',
        age=3,
        gender='male',
        status='available'
    )
    
    with app.app_context():
        db.session.add(pet)
        db.session.commit()
        yield pet

def test_admin_access_pets_list(client, admin_user):
    """Test that admin can access pets list"""
    # Login as admin
    client.post('/login', data={
        'username': 'admin',
        'password': 'password123'
    })
    
    response = client.get('/admin/pets')
    assert response.status_code == 200

def test_employee_cannot_access_admin_pets(client, employee_user):
    """Test that employee cannot access admin pets list"""
    # Login as employee
    client.post('/login', data={
        'username': 'employee',
        'password': 'password123'
    })
    
    response = client.get('/admin/pets')
    # Should redirect to login or show access denied
    assert response.status_code in [302, 403]

def test_employee_can_access_employee_pets(client, employee_user):
    """Test that employee can access employee pets list"""
    # Login as employee
    client.post('/login', data={
        'username': 'employee',
        'password': 'password123'
    })
    
    response = client.get('/employee/pets')
    assert response.status_code == 200

def test_employee_can_create_donation(client, employee_user):
    """Test that employee can create their own donation"""
    # Login as employee
    client.post('/login', data={
        'username': 'employee',
        'password': 'password123'
    })
    
    response = client.post('/employee/donate', data={
        'amount': '50.00',
        'donor_name': 'Test Donor',
        'donor_email': 'donor@test.com',
        'purpose': 'Test donation'
    })
    
    # Should redirect to dashboard or show success
    assert response.status_code in [200, 302]

def test_employee_cannot_delete_pet(client, employee_user, sample_pet):
    """Test that employee cannot delete pets"""
    # Login as employee
    client.post('/login', data={
        'username': 'employee',
        'password': 'password123'
    })
    
    response = client.post(f'/admin/pets/{sample_pet.pet_id}/delete')
    # Should not be able to access this endpoint
    assert response.status_code in [302, 403, 404]

def test_admin_can_delete_pet(client, admin_user, sample_pet):
    """Test that admin can delete pets"""
    # Login as admin
    client.post('/login', data={
        'username': 'admin',
        'password': 'password123'
    })
    
    response = client.post(f'/admin/pets/{sample_pet.pet_id}/delete')
    # Should be able to delete
    assert response.status_code in [200, 302]

def test_employee_can_view_own_donations(client, employee_user):
    """Test that employee can view their own donations"""
    # Create a donation for the employee
    with client.application.app_context():
        donation = Donation(
            amount=100.00,
            donor_name='Test Donor',
            donor_email='test@test.com',
            user_id=employee_user.id
        )
        db.session.add(donation)
        db.session.commit()
    
    # Login as employee
    client.post('/login', data={
        'username': 'employee',
        'password': 'password123'
    })
    
    response = client.get('/employee/my-donations')
    assert response.status_code == 200

def test_unauthorized_access_redirects(client):
    """Test that unauthorized access redirects to login"""
    # Try to access admin dashboard without login
    response = client.get('/admin/dashboard')
    assert response.status_code == 302  # Redirect to login

def test_admin_dashboard_access(client, admin_user):
    """Test admin dashboard access"""
    # Login as admin
    client.post('/login', data={
        'username': 'admin',
        'password': 'password123'
    })
    
    response = client.get('/admin/dashboard')
    assert response.status_code == 200

def test_employee_dashboard_access(client, employee_user):
    """Test employee dashboard access"""
    # Login as employee
    client.post('/login', data={
        'username': 'employee',
        'password': 'password123'
    })
    
    response = client.get('/employee/dashboard')
    assert response.status_code == 200
