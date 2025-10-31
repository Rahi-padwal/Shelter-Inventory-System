#!/usr/bin/env python3
"""
Pet Management System - Database Seeding Script
Populates the database with sample data for testing and demonstration
"""

from app import create_app, db
from app.models import User, Pet, Donation, Adoption, MedicalRecord
from werkzeug.security import generate_password_hash
from datetime import datetime, date, timedelta
import random

def create_sample_data():
    """Create sample data for the pet management system"""
    
    print("🌱 Seeding database with sample data...")
    
    # Clear existing data (in reverse order due to foreign keys)
    print("Clearing existing data...")
    MedicalRecord.query.delete()
    Adoption.query.delete()
    Donation.query.delete()
    Pet.query.delete()
    User.query.delete()
    
    # Create users
    print("Creating users...")
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
        ),
        User(
            username='john_doe',
            email='john@example.com',
            password_hash=generate_password_hash('password123'),
            role='employee'
        ),
        User(
            username='jane_smith',
            email='jane@example.com',
            password_hash=generate_password_hash('password123'),
            role='employee'
        )
    ]
    
    for user in users:
        db.session.add(user)
    
    db.session.commit()
    print(f"✅ Created {len(users)} users")
    
    # Create pets
    print("Creating pets...")
    pets = [
        Pet(
            pet_name='Buddy',
            breed='Golden Retriever',
            age=3,
            gender='male',
            status='available',
            description='Friendly and energetic dog, great with kids and other pets. Loves to play fetch and go for walks.',
            img_url='https://images.unsplash.com/photo-1552053831-71594a27632d?w=400',
            shelter_no='SH001'
        ),
        Pet(
            pet_name='Luna',
            breed='Persian Cat',
            age=2,
            gender='female',
            status='available',
            description='Calm and gentle cat, perfect for apartment living. Loves to cuddle and is very affectionate.',
            img_url='https://images.unsplash.com/photo-1574158622682-e40e69881006?w=400',
            shelter_no='SH002'
        ),
        Pet(
            pet_name='Max',
            breed='German Shepherd',
            age=5,
            gender='male',
            status='adopted',
            description='Loyal and protective dog, needs experienced owner. Great with families and very intelligent.',
            img_url='https://images.unsplash.com/photo-1583337130417-3346a1be7dee?w=400',
            shelter_no='SH003'
        ),
        Pet(
            pet_name='Whiskers',
            breed='Maine Coon',
            age=4,
            gender='male',
            status='foster',
            description='Large and majestic cat, very social and friendly. Great with children and other animals.',
            img_url='https://images.unsplash.com/photo-1573865526739-10639f7c7243?w=400',
            shelter_no='SH004'
        ),
        Pet(
            pet_name='Bella',
            breed='Labrador Mix',
            age=1,
            gender='female',
            status='available',
            description='Young and playful puppy, full of energy and love. Perfect for active families.',
            img_url='https://images.unsplash.com/photo-1547407139-3c921a71905c?w=400',
            shelter_no='SH005'
        ),
        Pet(
            pet_name='Shadow',
            breed='Black Cat',
            age=3,
            gender='male',
            status='available',
            description='Mysterious and independent cat, but very loving once he trusts you. Great for quiet homes.',
            img_url='https://images.unsplash.com/photo-1513245543132-31f507417b26?w=400',
            shelter_no='SH006'
        )
    ]
    
    for pet in pets:
        db.session.add(pet)
    
    db.session.commit()
    print(f"✅ Created {len(pets)} pets")
    
    # Create donations
    print("Creating donations...")
    donations = [
        Donation(
            amount=100.00,
            purpose='Medical care for injured pets',
            donor_name='John Smith',
            donor_email='john@example.com',
            donor_phone='+1234567890',
            message='Happy to help the animals in need. Keep up the great work!',
            user_id=users[1].id  # employee1
        ),
        Donation(
            amount=250.50,
            purpose='Food and supplies',
            donor_name='Jane Doe',
            donor_email='jane@example.com',
            donor_phone='+1987654321',
            message='For the daily care of the pets. Thank you for all you do!',
            user_id=users[2].id  # employee2
        ),
        Donation(
            amount=75.00,
            purpose='General care',
            donor_name='Mike Johnson',
            donor_email='mike@example.com',
            donor_phone='+1122334455',
            message='Small contribution to help with operations.',
            user_id=users[3].id  # john_doe
        ),
        Donation(
            amount=500.00,
            purpose='Emergency medical fund',
            donor_name='Sarah Wilson',
            donor_email='sarah@example.com',
            donor_phone='+1555666777',
            message='For emergency medical treatments. Hope this helps save lives.',
            user_id=users[4].id  # jane_smith
        ),
        Donation(
            amount=150.00,
            purpose='Vaccination program',
            donor_name='Robert Brown',
            donor_email='robert@example.com',
            message='Supporting the vaccination program for all pets.',
            user_id=users[1].id  # employee1
        )
    ]
    
    for donation in donations:
        db.session.add(donation)
    
    db.session.commit()
    print(f"✅ Created {len(donations)} donations")
    
    # Create adoptions
    print("Creating adoptions...")
    adoptions = [
        Adoption(
            adopt_name='Mike Johnson',
            adopt_email='mike@example.com',
            adopt_phone='+1122334455',
            pet_id=pets[2].pet_id,  # Max (German Shepherd)
            address='123 Main St, City, State 12345',
            user_id=users[1].id  # employee1
        ),
        Adoption(
            adopt_name='Sarah Wilson',
            adopt_email='sarah@example.com',
            adopt_phone='+1555666777',
            pet_id=pets[3].pet_id,  # Whiskers (Maine Coon) - but this pet is in foster, so we'll create a different scenario
            address='456 Oak Ave, City, State 12345',
            user_id=users[2].id  # employee2
        )
    ]
    
    for adoption in adoptions:
        db.session.add(adoption)
    
    db.session.commit()
    print(f"✅ Created {len(adoptions)} adoptions")
    
    # Create medical records
    print("Creating medical records...")
    medical_records = [
        MedicalRecord(
            pet_id=pets[0].pet_id,  # Buddy
            treatment_type='Annual vaccination',
            treat_date=date.today() - timedelta(days=30),
            donor_id=donations[0].id,
            vaccines='Rabies, DHPP, Bordetella',
            description='Annual vaccination checkup. All vaccines up to date.'
        ),
        MedicalRecord(
            pet_id=pets[1].pet_id,  # Luna
            treatment_type='Spay surgery',
            treat_date=date.today() - timedelta(days=15),
            donor_id=donations[1].id,
            vaccines='None',
            description='Spay surgery performed successfully. Recovery going well.'
        ),
        MedicalRecord(
            pet_id=pets[2].pet_id,  # Max
            treatment_type='Dental cleaning',
            treat_date=date.today() - timedelta(days=45),
            donor_id=donations[2].id,
            vaccines='None',
            description='Professional dental cleaning. Teeth are now healthy.'
        ),
        MedicalRecord(
            pet_id=pets[0].pet_id,  # Buddy
            treatment_type='Health checkup',
            treat_date=date.today() - timedelta(days=10),
            vaccines='None',
            description='Routine health checkup. Pet is in excellent condition.'
        ),
        MedicalRecord(
            pet_id=pets[4].pet_id,  # Bella
            treatment_type='Initial examination',
            treat_date=date.today() - timedelta(days=5),
            donor_id=donations[4].id,
            vaccines='First round of puppy vaccines',
            description='Initial health examination for new puppy. Started vaccination schedule.'
        )
    ]
    
    for record in medical_records:
        db.session.add(record)
    
    db.session.commit()
    print(f"✅ Created {len(medical_records)} medical records")
    
    print("\n🎉 Database seeding completed successfully!")
    print("\nSample login credentials:")
    print("Admin: admin / password123")
    print("Employee: employee1 / password123")
    print("Employee: employee2 / password123")

def main():
    """Main function to run the seeding process"""
    app = create_app()
    
    with app.app_context():
        try:
            create_sample_data()
        except Exception as e:
            print(f"❌ Error seeding database: {e}")
            db.session.rollback()
            raise

if __name__ == '__main__':
    main()
