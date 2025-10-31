from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import User, Pet, Donation, Adoption, MedicalRecord
from app.utils import save_uploaded_file, delete_uploaded_file
from datetime import datetime, date
from functools import wraps

admin_bp = Blueprint('admin', __name__)

def admin_required(f):
    """Decorator to require admin role"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            flash('Admin access required.', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    """Admin dashboard with statistics"""
    # Get counts for dashboard
    pets_count = Pet.query.count()
    adoptions_count = Adoption.query.count()
    donations_count = Donation.query.count()
    medical_records_count = MedicalRecord.query.count()
    
    # Recent activities
    recent_pets = Pet.query.order_by(Pet.created_at.desc()).limit(5).all()
    recent_adoptions = Adoption.query.order_by(Adoption.date.desc()).limit(5).all()
    recent_donations = Donation.query.order_by(Donation.date.desc()).limit(5).all()
    recent_medical = MedicalRecord.query.order_by(MedicalRecord.created_at.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html',
                         pets_count=pets_count,
                         adoptions_count=adoptions_count,
                         donations_count=donations_count,
                         medical_records_count=medical_records_count,
                         recent_pets=recent_pets,
                         recent_adoptions=recent_adoptions,
                         recent_donations=recent_donations,
                         recent_medical=recent_medical)

@admin_bp.route('/pets')
@login_required
@admin_required
def pets_list():
    """List all pets"""
    pets = Pet.query.order_by(Pet.created_at.desc()).all()
    return render_template('admin/pets_list.html', pets=pets)

@admin_bp.route('/pets/<int:pet_id>')
@login_required
@admin_required
def pet_detail(pet_id):
    """Get pet details"""
    pet = Pet.query.get_or_404(pet_id)
    medical_records = MedicalRecord.query.filter_by(pet_id=pet_id).order_by(MedicalRecord.treat_date.desc()).all()
    return render_template('admin/pet_detail.html', pet=pet, medical_records=medical_records)

@admin_bp.route('/pets/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_pet():
    """Create new pet"""
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        
        # Validation
        required_fields = ['pet_name', 'breed', 'age', 'gender']
        for field in required_fields:
            if not data.get(field):
                error_msg = f'{field.replace("_", " ").title()} is required'
                if request.is_json:
                    return jsonify({'error': error_msg}), 400
                flash(error_msg, 'error')
                return render_template('admin/create_pet.html')
        
        try:
            age = int(data.get('age'))
            if age < 0:
                raise ValueError('Age must be positive')
        except ValueError:
            error_msg = 'Age must be a valid positive number'
            if request.is_json:
                return jsonify({'error': error_msg}), 400
            flash(error_msg, 'error')
            return render_template('admin/create_pet.html')
        
        # Handle image upload
        img_url = data.get('img_url')  # URL input
        uploaded_file = request.files.get('pet_image')
        
        if uploaded_file and uploaded_file.filename:
            # Save uploaded file
            try:
                uploaded_url = save_uploaded_file(uploaded_file)
                if uploaded_url:
                    img_url = uploaded_url
                else:
                    error_msg = 'Invalid file type. Please upload PNG, JPG, JPEG, GIF, or WebP images only.'
                    if request.is_json:
                        return jsonify({'error': error_msg}), 400
                    flash(error_msg, 'error')
                    return render_template('admin/create_pet.html')
            except Exception as e:
                error_msg = 'Failed to upload image. Please try again.'
                if request.is_json:
                    return jsonify({'error': error_msg}), 400
                flash(error_msg, 'error')
                return render_template('admin/create_pet.html')
        elif not img_url:
            img_url = None
        
        pet = Pet(
            pet_name=data.get('pet_name'),
            breed=data.get('breed'),
            age=age,
            gender=data.get('gender'),
            status=data.get('status', 'available'),
            description=data.get('description'),
            img_url=img_url,
            shelter_no=data.get('shelter_no')
        )
        
        try:
            db.session.add(pet)
            db.session.commit()
            
            if request.is_json:
                return jsonify({'success': True, 'pet_id': pet.pet_id})
            
            flash('Pet created successfully!', 'success')
            return redirect(url_for('admin.pet_detail', pet_id=pet.pet_id))
            
        except Exception as e:
            db.session.rollback()
            error_msg = 'Failed to create pet. Please try again.'
            if request.is_json:
                return jsonify({'error': error_msg}), 500
            flash(error_msg, 'error')
    
    return render_template('admin/create_pet.html')

@admin_bp.route('/pets/<int:pet_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_pet(pet_id):
    """Edit pet"""
    pet = Pet.query.get_or_404(pet_id)
    
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        
        # Validation
        required_fields = ['pet_name', 'breed', 'age', 'gender']
        for field in required_fields:
            if not data.get(field):
                error_msg = f'{field.replace("_", " ").title()} is required'
                if request.is_json:
                    return jsonify({'error': error_msg}), 400
                flash(error_msg, 'error')
                return render_template('admin/edit_pet.html', pet=pet)
        
        try:
            age = int(data.get('age'))
            if age < 0:
                raise ValueError('Age must be positive')
        except ValueError:
            error_msg = 'Age must be a valid positive number'
            if request.is_json:
                return jsonify({'error': error_msg}), 400
            flash(error_msg, 'error')
            return render_template('admin/edit_pet.html', pet=pet)
        
        # Handle image upload
        img_url = data.get('img_url')  # URL input
        uploaded_file = request.files.get('pet_image')
        
        if uploaded_file and uploaded_file.filename:
            # Delete old image if exists
            if pet.img_url:
                delete_uploaded_file(pet.img_url)
            
            # Save new uploaded file
            try:
                uploaded_url = save_uploaded_file(uploaded_file)
                if uploaded_url:
                    img_url = uploaded_url
                else:
                    error_msg = 'Invalid file type. Please upload PNG, JPG, JPEG, GIF, or WebP images only.'
                    if request.is_json:
                        return jsonify({'error': error_msg}), 400
                    flash(error_msg, 'error')
                    return render_template('admin/edit_pet.html', pet=pet)
            except Exception as e:
                error_msg = 'Failed to upload image. Please try again.'
                if request.is_json:
                    return jsonify({'error': error_msg}), 400
                flash(error_msg, 'error')
                return render_template('admin/edit_pet.html', pet=pet)
        elif not img_url:
            img_url = pet.img_url  # Keep existing image if no new one provided
        
        # Update pet
        pet.pet_name = data.get('pet_name')
        pet.breed = data.get('breed')
        pet.age = age
        pet.gender = data.get('gender')
        pet.status = data.get('status', 'available')
        pet.description = data.get('description')
        pet.img_url = img_url
        pet.shelter_no = data.get('shelter_no')
        
        try:
            db.session.commit()
            
            if request.is_json:
                return jsonify({'success': True})
            
            flash('Pet updated successfully!', 'success')
            return redirect(url_for('admin.pet_detail', pet_id=pet.pet_id))
            
        except Exception as e:
            db.session.rollback()
            error_msg = 'Failed to update pet. Please try again.'
            if request.is_json:
                return jsonify({'error': error_msg}), 500
            flash(error_msg, 'error')
    
    return render_template('admin/edit_pet.html', pet=pet)

@admin_bp.route('/pets/<int:pet_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_pet(pet_id):
    """Delete pet"""
    pet = Pet.query.get_or_404(pet_id)
    
    try:
        # Delete related records first
        MedicalRecord.query.filter_by(pet_id=pet_id).delete()
        Adoption.query.filter_by(pet_id=pet_id).delete()
        
        db.session.delete(pet)
        db.session.commit()
        
        if request.is_json:
            return jsonify({'success': True})
        
        flash('Pet deleted successfully!', 'success')
        return redirect(url_for('admin.pets_list'))
        
    except Exception as e:
        db.session.rollback()
        error_msg = 'Failed to delete pet. Please try again.'
        if request.is_json:
            return jsonify({'error': error_msg}), 500
        flash(error_msg, 'error')
        return redirect(url_for('admin.pets_list'))

@admin_bp.route('/donations')
@login_required
@admin_required
def donations_list():
    """List all donations"""
    donations = Donation.query.order_by(Donation.date.desc()).all()
    return render_template('admin/donations_list.html', donations=donations)

@admin_bp.route('/donations/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_donation():
    """Create new donation"""
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
                return render_template('admin/create_donation.html')
        
        try:
            amount = float(data.get('amount'))
            if amount <= 0:
                raise ValueError('Amount must be positive')
        except ValueError:
            error_msg = 'Amount must be a valid positive number'
            if request.is_json:
                return jsonify({'error': error_msg}), 400
            flash(error_msg, 'error')
            return render_template('admin/create_donation.html')
        
        donation = Donation(
            amount=amount,
            purpose=data.get('purpose'),
            donor_name=data.get('donor_name'),
            donor_email=data.get('donor_email'),
            donor_phone=data.get('donor_phone'),
            message=data.get('message')
        )
        
        try:
            db.session.add(donation)
            db.session.commit()
            
            if request.is_json:
                return jsonify({'success': True, 'donation_id': donation.id})
            
            flash('Donation created successfully!', 'success')
            return redirect(url_for('admin.donations_list'))
            
        except Exception as e:
            db.session.rollback()
            error_msg = 'Failed to create donation. Please try again.'
            if request.is_json:
                return jsonify({'error': error_msg}), 500
            flash(error_msg, 'error')
    
    return render_template('admin/create_donation.html')

@admin_bp.route('/adoptions')
@login_required
@admin_required
def adoptions_list():
    """List all adoptions"""
    adoptions = Adoption.query.order_by(Adoption.date.desc()).all()
    return render_template('admin/adoptions_list.html', adoptions=adoptions)

@admin_bp.route('/adoptions/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_adoption():
    """Create new adoption"""
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        
        # Validation
        required_fields = ['adopt_name', 'adopt_email', 'pet_id']
        for field in required_fields:
            if not data.get(field):
                error_msg = f'{field.replace("_", " ").title()} is required'
                if request.is_json:
                    return jsonify({'error': error_msg}), 400
                flash(error_msg, 'error')
                return render_template('admin/create_adoption.html', pets=Pet.query.all())
        
        # Check if pet exists and is available
        pet = Pet.query.get(data.get('pet_id'))
        if not pet:
            error_msg = 'Selected pet does not exist'
            if request.is_json:
                return jsonify({'error': error_msg}), 400
            flash(error_msg, 'error')
            return render_template('admin/create_adoption.html', pets=Pet.query.all())
        
        if pet.status != 'available':
            error_msg = 'Selected pet is not available for adoption'
            if request.is_json:
                return jsonify({'error': error_msg}), 400
            flash(error_msg, 'error')
            return render_template('admin/create_adoption.html', pets=Pet.query.all())
        
        adoption = Adoption(
            adopt_name=data.get('adopt_name'),
            adopt_email=data.get('adopt_email'),
            adopt_phone=data.get('adopt_phone'),
            pet_id=data.get('pet_id'),
            address=data.get('address')
        )
        
        try:
            db.session.add(adoption)
            # Update pet status
            pet.status = 'adopted'
            db.session.commit()
            
            if request.is_json:
                return jsonify({'success': True, 'adoption_id': adoption.id})
            
            flash('Adoption created successfully!', 'success')
            return redirect(url_for('admin.adoptions_list'))
            
        except Exception as e:
            db.session.rollback()
            error_msg = 'Failed to create adoption. Please try again.'
            if request.is_json:
                return jsonify({'error': error_msg}), 500
            flash(error_msg, 'error')
    
    return render_template('admin/create_adoption.html', pets=Pet.query.all())

@admin_bp.route('/medical-records')
@login_required
@admin_required
def medical_records_list():
    """List all medical records"""
    medical_records = MedicalRecord.query.order_by(MedicalRecord.created_at.desc()).all()
    return render_template('admin/medical_records_list.html', medical_records=medical_records)

@admin_bp.route('/medical-records/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_medical_record():
    """Create new medical record"""
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        
        # Validation
        required_fields = ['pet_id', 'treatment_type', 'treat_date']
        for field in required_fields:
            if not data.get(field):
                error_msg = f'{field.replace("_", " ").title()} is required'
                if request.is_json:
                    return jsonify({'error': error_msg}), 400
                flash(error_msg, 'error')
                return render_template('admin/create_medical_record.html', 
                                     pets=Pet.query.all(), 
                                     donations=Donation.query.all())
        
        # Check if pet exists
        pet = Pet.query.get(data.get('pet_id'))
        if not pet:
            error_msg = 'Selected pet does not exist'
            if request.is_json:
                return jsonify({'error': error_msg}), 400
            flash(error_msg, 'error')
            return render_template('admin/create_medical_record.html', 
                                 pets=Pet.query.all(), 
                                 donations=Donation.query.all())
        
        # Parse date
        try:
            treat_date = datetime.strptime(data.get('treat_date'), '%Y-%m-%d').date()
        except ValueError:
            error_msg = 'Invalid date format. Use YYYY-MM-DD'
            if request.is_json:
                return jsonify({'error': error_msg}), 400
            flash(error_msg, 'error')
            return render_template('admin/create_medical_record.html', 
                                 pets=Pet.query.all(), 
                                 donations=Donation.query.all())
        
        medical_record = MedicalRecord(
            pet_id=data.get('pet_id'),
            treatment_type=data.get('treatment_type'),
            treat_date=treat_date,
            donor_id=data.get('donor_id') if data.get('donor_id') else None,
            vaccines=data.get('vaccines'),
            description=data.get('description')
        )
        
        try:
            db.session.add(medical_record)
            db.session.commit()
            
            if request.is_json:
                return jsonify({'success': True, 'medical_record_id': medical_record.id})
            
            flash('Medical record created successfully!', 'success')
            return redirect(url_for('admin.medical_records_list'))
            
        except Exception as e:
            db.session.rollback()
            error_msg = 'Failed to create medical record. Please try again.'
            if request.is_json:
                return jsonify({'error': error_msg}), 500
            flash(error_msg, 'error')
    
    return render_template('admin/create_medical_record.html', 
                         pets=Pet.query.all(), 
                         donations=Donation.query.all())
