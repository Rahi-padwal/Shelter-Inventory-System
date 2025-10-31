from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import User, Pet, Donation, Adoption, MedicalRecord
from datetime import datetime, date
from functools import wraps
import re

employee_bp = Blueprint('employee', __name__)

def employee_required(f):
    """Decorator to require employee role"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_employee():
            flash('Employee access required.', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone(phone):
    """Validate phone number format"""
    pattern = r'^[\+]?[1-9][\d]{0,15}$'
    return re.match(pattern, phone) is not None

@employee_bp.route('/dashboard')
@login_required
@employee_required
def dashboard():
    """Employee dashboard with limited statistics"""
    # Get counts for dashboard (only user's own records)
    user_donations_count = Donation.query.filter_by(user_id=current_user.id).count()
    user_adoptions_count = Adoption.query.filter_by(user_id=current_user.id).count()
    pets_count = Pet.query.count()
    medical_records_count = MedicalRecord.query.count()
    
    # Recent activities
    recent_pets = Pet.query.order_by(Pet.created_at.desc()).limit(5).all()
    user_recent_donations = Donation.query.filter_by(user_id=current_user.id).order_by(Donation.date.desc()).limit(5).all()
    user_recent_adoptions = Adoption.query.filter_by(user_id=current_user.id).order_by(Adoption.date.desc()).limit(5).all()
    recent_medical = MedicalRecord.query.order_by(MedicalRecord.created_at.desc()).limit(5).all()
    
    return render_template('employee/dashboard.html',
                         pets_count=pets_count,
                         user_donations_count=user_donations_count,
                         user_adoptions_count=user_adoptions_count,
                         medical_records_count=medical_records_count,
                         recent_pets=recent_pets,
                         user_recent_donations=user_recent_donations,
                         user_recent_adoptions=user_recent_adoptions,
                         recent_medical=recent_medical)

@employee_bp.route('/pets')
@login_required
@employee_required
def pets_list():
    """List all pets (read-only for employees)"""
    pets = Pet.query.order_by(Pet.created_at.desc()).all()
    return render_template('employee/pets_list.html', pets=pets)

@employee_bp.route('/pets/<int:pet_id>')
@login_required
@employee_required
def pet_detail(pet_id):
    """View pet details (read-only for employees)"""
    pet = Pet.query.get_or_404(pet_id)
    medical_records = MedicalRecord.query.filter_by(pet_id=pet_id).order_by(MedicalRecord.treat_date.desc()).all()
    return render_template('employee/pet_detail.html', pet=pet, medical_records=medical_records)

@employee_bp.route('/donate', methods=['GET', 'POST'])
@login_required
@employee_required
def donate():
    """Create donation (employees can create their own donations)"""
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        
        # Validation
        required_fields = ['amount', 'donor_name', 'donor_email']
        for field in required_fields:
            if not data.get(field):
                error_msg = f'{field.replace("_", " ").title()} is required'
                if request.is_json:
                    return jsonify({'error': error_msg}), 400
                flash(error_msg, 'error')
                return render_template('employee/donate.html')
        
        # Validate email
        if not validate_email(data.get('donor_email')):
            error_msg = 'Invalid email format'
            if request.is_json:
                return jsonify({'error': error_msg}), 400
            flash(error_msg, 'error')
            return render_template('employee/donate.html')
        
        # Validate phone if provided
        if data.get('donor_phone') and not validate_phone(data.get('donor_phone')):
            error_msg = 'Invalid phone number format'
            if request.is_json:
                return jsonify({'error': error_msg}), 400
            flash(error_msg, 'error')
            return render_template('employee/donate.html')
        
        try:
            amount = float(data.get('amount'))
            if amount <= 0:
                raise ValueError('Amount must be positive')
        except ValueError:
            error_msg = 'Amount must be a valid positive number'
            if request.is_json:
                return jsonify({'error': error_msg}), 400
            flash(error_msg, 'error')
            return render_template('employee/donate.html')
        
        donation = Donation(
            amount=amount,
            purpose=data.get('purpose'),
            donor_name=data.get('donor_name'),
            donor_email=data.get('donor_email'),
            donor_phone=data.get('donor_phone'),
            message=data.get('message'),
            user_id=current_user.id  # Link to current user
        )
        
        try:
            db.session.add(donation)
            db.session.commit()
            
            if request.is_json:
                return jsonify({'success': True, 'donation_id': donation.id})
            
            flash('Donation created successfully!', 'success')
            return redirect(url_for('employee.dashboard'))
            
        except Exception as e:
            db.session.rollback()
            error_msg = 'Failed to create donation. Please try again.'
            if request.is_json:
                return jsonify({'error': error_msg}), 500
            flash(error_msg, 'error')
    
    return render_template('employee/donate.html')

@employee_bp.route('/adopt')
@login_required
@employee_required
def adopt_pets_list():
    """List available pets for adoption"""
    pets = Pet.query.filter_by(status='available').order_by(Pet.created_at.desc()).all()
    return render_template('employee/adopt_pets_list.html', pets=pets)

@employee_bp.route('/adopt/<int:pet_id>', methods=['GET', 'POST'])
@login_required
@employee_required
def adopt_pet(pet_id):
    """Adopt a specific pet"""
    pet = Pet.query.get_or_404(pet_id)
    
    if pet.status != 'available':
        flash('This pet is not available for adoption.', 'error')
        return redirect(url_for('employee.adopt_pets_list'))
    
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        
        # Validation
        required_fields = ['adopt_name', 'adopt_email']
        for field in required_fields:
            if not data.get(field):
                error_msg = f'{field.replace("_", " ").title()} is required'
                if request.is_json:
                    return jsonify({'error': error_msg}), 400
                flash(error_msg, 'error')
                return render_template('employee/adopt_pet.html', pet=pet)
        
        # Validate email
        if not validate_email(data.get('adopt_email')):
            error_msg = 'Invalid email format'
            if request.is_json:
                return jsonify({'error': error_msg}), 400
            flash(error_msg, 'error')
            return render_template('employee/adopt_pet.html', pet=pet)
        
        # Validate phone if provided
        if data.get('adopt_phone') and not validate_phone(data.get('adopt_phone')):
            error_msg = 'Invalid phone number format'
            if request.is_json:
                return jsonify({'error': error_msg}), 400
            flash(error_msg, 'error')
            return render_template('employee/adopt_pet.html', pet=pet)
        
        adoption = Adoption(
            adopt_name=data.get('adopt_name'),
            adopt_email=data.get('adopt_email'),
            adopt_phone=data.get('adopt_phone'),
            pet_id=pet_id,
            address=data.get('address'),
            user_id=current_user.id  # Link to current user
        )
        
        try:
            db.session.add(adoption)
            # Update pet status
            pet.status = 'adopted'
            db.session.commit()
            
            if request.is_json:
                return jsonify({'success': True, 'adoption_id': adoption.id})
            
            flash('Adoption created successfully!', 'success')
            return redirect(url_for('employee.dashboard'))
            
        except Exception as e:
            db.session.rollback()
            error_msg = 'Failed to create adoption. Please try again.'
            if request.is_json:
                return jsonify({'error': error_msg}), 500
            flash(error_msg, 'error')
    
    return render_template('employee/adopt_pet.html', pet=pet)

@employee_bp.route('/medical-records')
@login_required
@employee_required
def medical_records_list():
    """List medical records (read-only for employees)"""
    medical_records = MedicalRecord.query.order_by(MedicalRecord.created_at.desc()).all()
    return render_template('employee/medical_records_list.html', medical_records=medical_records)

@employee_bp.route('/my-donations')
@login_required
@employee_required
def my_donations():
    """List employee's own donations"""
    donations = Donation.query.filter_by(user_id=current_user.id).order_by(Donation.date.desc()).all()
    return render_template('employee/my_donations.html', donations=donations)

@employee_bp.route('/my-adoptions')
@login_required
@employee_required
def my_adoptions():
    """List employee's own adoptions"""
    adoptions = Adoption.query.filter_by(user_id=current_user.id).order_by(Adoption.date.desc()).all()
    return render_template('employee/my_adoptions.html', adoptions=adoptions)

@employee_bp.route('/my-donations/<int:donation_id>/edit', methods=['GET', 'POST'])
@login_required
@employee_required
def edit_my_donation(donation_id):
    """Edit employee's own donation"""
    donation = Donation.query.filter_by(id=donation_id, user_id=current_user.id).first_or_404()
    
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        
        # Validation
        required_fields = ['amount', 'donor_name', 'donor_email']
        for field in required_fields:
            if not data.get(field):
                error_msg = f'{field.replace("_", " ").title()} is required'
                if request.is_json:
                    return jsonify({'error': error_msg}), 400
                flash(error_msg, 'error')
                return render_template('employee/edit_donation.html', donation=donation)
        
        # Validate email
        if not validate_email(data.get('donor_email')):
            error_msg = 'Invalid email format'
            if request.is_json:
                return jsonify({'error': error_msg}), 400
            flash(error_msg, 'error')
            return render_template('employee/edit_donation.html', donation=donation)
        
        # Validate phone if provided
        if data.get('donor_phone') and not validate_phone(data.get('donor_phone')):
            error_msg = 'Invalid phone number format'
            if request.is_json:
                return jsonify({'error': error_msg}), 400
            flash(error_msg, 'error')
            return render_template('employee/edit_donation.html', donation=donation)
        
        try:
            amount = float(data.get('amount'))
            if amount <= 0:
                raise ValueError('Amount must be positive')
        except ValueError:
            error_msg = 'Amount must be a valid positive number'
            if request.is_json:
                return jsonify({'error': error_msg}), 400
            flash(error_msg, 'error')
            return render_template('employee/edit_donation.html', donation=donation)
        
        # Update donation
        donation.amount = amount
        donation.purpose = data.get('purpose')
        donation.donor_name = data.get('donor_name')
        donation.donor_email = data.get('donor_email')
        donation.donor_phone = data.get('donor_phone')
        donation.message = data.get('message')
        
        try:
            db.session.commit()
            
            if request.is_json:
                return jsonify({'success': True})
            
            flash('Donation updated successfully!', 'success')
            return redirect(url_for('employee.my_donations'))
            
        except Exception as e:
            db.session.rollback()
            error_msg = 'Failed to update donation. Please try again.'
            if request.is_json:
                return jsonify({'error': error_msg}), 500
            flash(error_msg, 'error')
    
    return render_template('employee/edit_donation.html', donation=donation)

@employee_bp.route('/my-adoptions/<int:adoption_id>/edit', methods=['GET', 'POST'])
@login_required
@employee_required
def edit_my_adoption(adoption_id):
    """Edit employee's own adoption"""
    adoption = Adoption.query.filter_by(id=adoption_id, user_id=current_user.id).first_or_404()
    
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        
        # Validation
        required_fields = ['adopt_name', 'adopt_email']
        for field in required_fields:
            if not data.get(field):
                error_msg = f'{field.replace("_", " ").title()} is required'
                if request.is_json:
                    return jsonify({'error': error_msg}), 400
                flash(error_msg, 'error')
                return render_template('employee/edit_adoption.html', adoption=adoption)
        
        # Validate email
        if not validate_email(data.get('adopt_email')):
            error_msg = 'Invalid email format'
            if request.is_json:
                return jsonify({'error': error_msg}), 400
            flash(error_msg, 'error')
            return render_template('employee/edit_adoption.html', adoption=adoption)
        
        # Validate phone if provided
        if data.get('adopt_phone') and not validate_phone(data.get('adopt_phone')):
            error_msg = 'Invalid phone number format'
            if request.is_json:
                return jsonify({'error': error_msg}), 400
            flash(error_msg, 'error')
            return render_template('employee/edit_adoption.html', adoption=adoption)
        
        # Update adoption
        adoption.adopt_name = data.get('adopt_name')
        adoption.adopt_email = data.get('adopt_email')
        adoption.adopt_phone = data.get('adopt_phone')
        adoption.address = data.get('address')
        
        try:
            db.session.commit()
            
            if request.is_json:
                return jsonify({'success': True})
            
            flash('Adoption updated successfully!', 'success')
            return redirect(url_for('employee.my_adoptions'))
            
        except Exception as e:
            db.session.rollback()
            error_msg = 'Failed to update adoption. Please try again.'
            if request.is_json:
                return jsonify({'error': error_msg}), 500
            flash(error_msg, 'error')
    
    return render_template('employee/edit_adoption.html', adoption=adoption)
