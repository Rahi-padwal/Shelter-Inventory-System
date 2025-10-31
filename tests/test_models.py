"""
Test cases for database models
"""

import pytest
from app import create_app, db
from app.models import User, Pet, Donation, Adoption, MedicalRecord
from datetime import date, datetime

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

def test_user_model(app):
    """Test User model functionality"""
    with app.app_context():
        user = User(
            username='testuser',
            email='test@example.com',
            role='employee'
        )
        user.set_password('password123')
        
        db.session.add(user)
        db.session.commit()
        
        # Test password hashing
        assert user.check_password('password123')
        assert not user.check_password('wrongpassword')
        
        # Test role methods
        assert user.is_employee()
        assert not user.is_admin()
        
        # Test admin role
        admin_user = User(username='admin', email='admin@test.com', role='admin')
        admin_user.set_password('pass')
        db.session.add(admin_user)
        db.session.commit()
        
        assert admin_user.is_admin()
        assert not admin_user.is_employee()

def test_pet_model(app):
    """Test Pet model functionality"""
    with app.app_context():
        pet = Pet(
            pet_name='Buddy',
            breed='Golden Retriever',
            age=3,
            gender='male',
            status='available',
            description='Friendly dog',
            shelter_no='SH001'
        )
        
        db.session.add(pet)
        db.session.commit()
        
        # Test pet creation
        assert pet.pet_name == 'Buddy'
        assert pet.breed == 'Golden Retriever'
        assert pet.age == 3
        assert pet.gender == 'male'
        assert pet.status == 'available'
        
        # Test relationships
        assert pet.adoptions is not None
        assert pet.medical_records is not None

def test_donation_model(app):
    """Test Donation model functionality"""
    with app.app_context():
        # Create user first
        user = User(username='donor', email='donor@test.com', role='employee')
        user.set_password('pass')
        db.session.add(user)
        db.session.commit()
        
        donation = Donation(
            amount=100.50,
            purpose='Medical care',
            donor_name='John Doe',
            donor_email='john@example.com',
            donor_phone='+1234567890',
            message='Hope this helps',
            user_id=user.id
        )
        
        db.session.add(donation)
        db.session.commit()
        
        # Test donation creation
        assert donation.amount == 100.50
        assert donation.purpose == 'Medical care'
        assert donation.donor_name == 'John Doe'
        assert donation.user_id == user.id
        
        # Test relationships
        assert donation.donor_user == user
        assert donation.medical_records is not None

def test_adoption_model(app):
    """Test Adoption model functionality"""
    with app.app_context():
        # Create user and pet first
        user = User(username='adopter', email='adopter@test.com', role='employee')
        user.set_password('pass')
        db.session.add(user)
        
        pet = Pet(
            pet_name='Luna',
            breed='Persian Cat',
            age=2,
            gender='female',
            status='available'
        )
        db.session.add(pet)
        db.session.commit()
        
        adoption = Adoption(
            adopt_name='Jane Smith',
            adopt_email='jane@example.com',
            adopt_phone='+1987654321',
            pet_id=pet.pet_id,
            address='123 Main St',
            user_id=user.id
        )
        
        db.session.add(adoption)
        db.session.commit()
        
        # Test adoption creation
        assert adoption.adopt_name == 'Jane Smith'
        assert adoption.pet_id == pet.pet_id
        assert adoption.user_id == user.id
        
        # Test relationships
        assert adoption.pet == pet
        assert adoption.adopter_user == user

def test_medical_record_model(app):
    """Test MedicalRecord model functionality"""
    with app.app_context():
        # Create pet and donation first
        pet = Pet(
            pet_name='Max',
            breed='German Shepherd',
            age=5,
            gender='male',
            status='available'
        )
        db.session.add(pet)
        
        donation = Donation(
            amount=200.00,
            donor_name='Donor',
            donor_email='donor@test.com'
        )
        db.session.add(donation)
        db.session.commit()
        
        medical_record = MedicalRecord(
            pet_id=pet.pet_id,
            treatment_type='Vaccination',
            treat_date=date.today(),
            donor_id=donation.id,
            vaccines='Rabies, DHPP',
            description='Annual vaccination'
        )
        
        db.session.add(medical_record)
        db.session.commit()
        
        # Test medical record creation
        assert medical_record.pet_id == pet.pet_id
        assert medical_record.treatment_type == 'Vaccination'
        assert medical_record.donor_id == donation.id
        assert medical_record.vaccines == 'Rabies, DHPP'
        
        # Test relationships
        assert medical_record.pet == pet
        assert medical_record.donation == donation

def test_model_relationships(app):
    """Test model relationships work correctly"""
    with app.app_context():
        # Create user
        user = User(username='testuser', email='test@test.com', role='employee')
        user.set_password('pass')
        db.session.add(user)
        
        # Create pet
        pet = Pet(
            pet_name='Test Pet',
            breed='Test Breed',
            age=1,
            gender='male',
            status='available'
        )
        db.session.add(pet)
        
        # Create donation
        donation = Donation(
            amount=50.00,
            donor_name='Test Donor',
            donor_email='donor@test.com',
            user_id=user.id
        )
        db.session.add(donation)
        
        db.session.commit()
        
        # Create adoption
        adoption = Adoption(
            adopt_name='Adopter',
            adopt_email='adopter@test.com',
            pet_id=pet.pet_id,
            user_id=user.id
        )
        db.session.add(adoption)
        
        # Create medical record
        medical_record = MedicalRecord(
            pet_id=pet.pet_id,
            treatment_type='Checkup',
            treat_date=date.today(),
            donor_id=donation.id
        )
        db.session.add(medical_record)
        db.session.commit()
        
        # Test relationships
        assert len(user.donations.all()) == 1
        assert len(user.adoptions.all()) == 1
        assert len(pet.adoptions.all()) == 1
        assert len(pet.medical_records.all()) == 1
        assert len(donation.medical_records.all()) == 1

def test_model_validation(app):
    """Test model validation and constraints"""
    with app.app_context():
        # Test required fields
        pet = Pet()  # Missing required fields
        db.session.add(pet)
        
        with pytest.raises(Exception):
            db.session.commit()
        
        db.session.rollback()
        
        # Test valid pet creation
        pet = Pet(
            pet_name='Valid Pet',
            breed='Valid Breed',
            age=2,
            gender='female',
            status='available'
        )
        db.session.add(pet)
        db.session.commit()
        
        assert pet.pet_id is not None
