from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from app import db

class User(UserMixin, db.Model):
    """User model for authentication and role management"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.Enum('admin', 'employee', name='user_roles'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    donations = db.relationship('Donation', backref='donor_user', lazy='dynamic')
    adoptions = db.relationship('Adoption', backref='adopter_user', lazy='dynamic')
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check password against hash"""
        return check_password_hash(self.password_hash, password)
    
    def is_admin(self):
        """Check if user is admin"""
        return self.role == 'admin'
    
    def is_employee(self):
        """Check if user is employee"""
        return self.role == 'employee'
    
    def __repr__(self):
        return f'<User {self.username}>'

class Pet(db.Model):
    """Pet model for animal records"""
    __tablename__ = 'pets'
    
    pet_id = db.Column(db.Integer, primary_key=True)
    pet_name = db.Column(db.String(100), nullable=False)
    breed = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.Enum('male', 'female', name='pet_genders'), nullable=False)
    status = db.Column(db.Enum('available', 'adopted', 'foster', name='pet_status'), 
                      default='available', nullable=False)
    description = db.Column(db.Text)
    img_url = db.Column(db.String(500))
    shelter_no = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    adoptions = db.relationship('Adoption', backref='pet', lazy='dynamic')
    medical_records = db.relationship('MedicalRecord', backref='pet', lazy='dynamic')
    
    def __repr__(self):
        return f'<Pet {self.pet_name}>'

class Donation(db.Model):
    """Donation model for financial contributions"""
    __tablename__ = 'donations'
    
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    purpose = db.Column(db.String(200))
    donor_name = db.Column(db.String(100), nullable=False)
    donor_email = db.Column(db.String(120), nullable=False)
    donor_phone = db.Column(db.String(20))
    message = db.Column(db.Text)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    
    # Relationships
    medical_records = db.relationship('MedicalRecord', backref='donation', lazy='dynamic')
    
    def __repr__(self):
        return f'<Donation {self.amount} by {self.donor_name}>'

class Adoption(db.Model):
    """Adoption model for pet adoptions"""
    __tablename__ = 'adoptions'
    
    id = db.Column(db.Integer, primary_key=True)
    adopt_name = db.Column(db.String(100), nullable=False)
    adopt_email = db.Column(db.String(120), nullable=False)
    adopt_phone = db.Column(db.String(20))
    pet_id = db.Column(db.Integer, db.ForeignKey('pets.pet_id'), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    address = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    
    def __repr__(self):
        return f'<Adoption {self.adopt_name} -> Pet {self.pet_id}>'

class MedicalRecord(db.Model):
    """Medical record model for pet health tracking"""
    __tablename__ = 'medical_records'
    
    id = db.Column(db.Integer, primary_key=True)
    pet_id = db.Column(db.Integer, db.ForeignKey('pets.pet_id'), nullable=False)
    treatment_type = db.Column(db.String(200), nullable=False)
    treat_date = db.Column(db.Date, nullable=False)
    donor_id = db.Column(db.Integer, db.ForeignKey('donations.id'), nullable=True)
    vaccines = db.Column(db.Text)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<MedicalRecord {self.treatment_type} for Pet {self.pet_id}>'
