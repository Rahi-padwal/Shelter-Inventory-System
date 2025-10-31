#!/usr/bin/env python3
"""
Pet Management System - SQLite Setup Script
Quick setup using SQLite database (no MySQL required)
"""

from app import create_app, db
from app.models import User, Pet, Donation, Adoption, MedicalRecord
from werkzeug.security import generate_password_hash
from datetime import datetime, date, timedelta

def setup_sqlite_database():
    """Setup SQLite database with sample data"""
    
    print("🐕 Pet Management System - SQLite Setup")
    print("=" * 50)
    
    # Create uploads directory
    import os
    os.makedirs('static/uploads', exist_ok=True)
    print("✅ Created uploads directory")
    
    app = create_app()
    
    with app.app_context():
        # Drop all tables and recreate
        print("Creating database tables...")
        db.drop_all()
        db.create_all()
        
        # Create sample users
        print("Creating sample users...")
        users = [
            User(
                username='admin',
                email='admin@petmanagement.com',
                password_hash=generate_password_hash('password123'),
                role='admin'
            ),
            User(
                username='employee1',
                email='employee1@petmanagement.com',
                password_hash=generate_password_hash('password123'),
                role='employee'
            ),
            User(
                username='employee2',
                email='employee2@petmanagement.com',
                password_hash=generate_password_hash('password123'),
                role='employee'
            )
        ]
        
        for user in users:
            db.session.add(user)
        
        db.session.commit()
        print(f"✅ Created {len(users)} users")
        
        # Create sample pets
        print("Creating sample pets...")
        pets = [
            Pet(
                pet_name='Buddy',
                breed='Golden Retriever',
                age=3,
                gender='male',
                status='available',
                description='Friendly and energetic dog, great with kids and other pets.',
                img_url='https://images.unsplash.com/photo-1552053831-71594a27632d?w=400',
                shelter_no='SH001'
            ),
            Pet(
                pet_name='Luna',
                breed='Persian Cat',
                age=2,
                gender='female',
                status='available',
                description='Calm and gentle cat, perfect for apartment living.',
                img_url='https://images.unsplash.com/photo-1574158622682-e40e69881006?w=400',
                shelter_no='SH002'
            ),
            Pet(
                pet_name='Max',
                breed='German Shepherd',
                age=5,
                gender='male',
                status='adopted',
                description='Loyal and protective dog, needs experienced owner.',
                img_url='https://images.unsplash.com/photo-1583337130417-3346a1be7dee?w=400',
                shelter_no='SH003'
            )
        ]
        
        for pet in pets:
            db.session.add(pet)
        
        db.session.commit()
        print(f"✅ Created {len(pets)} pets")
        
        # Create sample donations
        print("Creating sample donations...")
        donations = [
            Donation(
                amount=100.00,
                purpose='Medical care for injured pets',
                donor_name='John Smith',
                donor_email='john@example.com',
                donor_phone='+1234567890',
                message='Happy to help the animals in need.',
                user_id=users[1].id  # employee1
            ),
            Donation(
                amount=250.50,
                purpose='Food and supplies',
                donor_name='Jane Doe',
                donor_email='jane@example.com',
                donor_phone='+1987654321',
                message='For the daily care of the pets.',
                user_id=users[2].id  # employee2
            )
        ]
        
        for donation in donations:
            db.session.add(donation)
        
        db.session.commit()
        print(f"✅ Created {len(donations)} donations")
        
        # Create sample adoption
        print("Creating sample adoption...")
        adoption = Adoption(
            adopt_name='Mike Johnson',
            adopt_email='mike@example.com',
            adopt_phone='+1122334455',
            pet_id=pets[2].pet_id,  # Max
            address='123 Main St, City, State 12345',
            user_id=users[1].id  # employee1
        )
        
        db.session.add(adoption)
        db.session.commit()
        print("✅ Created 1 adoption")
        
        # Create sample medical records
        print("Creating sample medical records...")
        medical_records = [
            MedicalRecord(
                pet_id=pets[0].pet_id,  # Buddy
                treatment_type='Annual vaccination',
                treat_date=date.today() - timedelta(days=30),
                donor_id=donations[0].id,
                vaccines='Rabies, DHPP, Bordetella',
                description='Annual vaccination checkup.'
            ),
            MedicalRecord(
                pet_id=pets[1].pet_id,  # Luna
                treatment_type='Spay surgery',
                treat_date=date.today() - timedelta(days=15),
                donor_id=donations[1].id,
                vaccines='None',
                description='Spay surgery performed successfully.'
            )
        ]
        
        for record in medical_records:
            db.session.add(record)
        
        db.session.commit()
        print(f"✅ Created {len(medical_records)} medical records")
        
        print("\n🎉 SQLite database setup completed successfully!")
        print("\nLogin credentials:")
        print("Admin: admin / password123")
        print("Employee: employee1 / password123")
        print("Employee: employee2 / password123")
        print("\nRun the application with: python run.py")

if __name__ == '__main__':
    setup_sqlite_database()
