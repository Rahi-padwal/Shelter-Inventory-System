# Pet Management System

A comprehensive web application for managing pet adoptions, donations, and medical records built with Flask, MySQL, and Bootstrap.

## Features

### 🔐 Authentication & Roles
- **Admin Role**: Full CRUD access to all system data
- **Employee Role**: Limited access to create/update their own donations and adoptions
- Secure password hashing with Flask-Login
- Role-based route protection

### 🐕 Pet Management
- Add, edit, and delete pet records
- Track pet status (available, adopted, foster)
- Upload pet images via URL
- Comprehensive pet information including breed, age, gender

### 💰 Donation System
- Record financial contributions
- Link donations to medical treatments
- Track donor information
- Employee-specific donation tracking

### ❤️ Adoption Process
- Manage pet adoptions
- Track adopter information
- Automatic pet status updates
- Employee adoption management

### 🏥 Medical Records
- Track pet medical treatments
- Link treatments to donations
- Vaccine tracking
- Treatment history

## Technology Stack

- **Backend**: Flask (Python)
- **Database**: MySQL
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Authentication**: Flask-Login
- **ORM**: SQLAlchemy
- **Database Migration**: Flask-Migrate

## Installation & Setup

### Prerequisites
- Python 3.8+
- MySQL 5.7+
- pip (Python package manager)

### 1. Clone the Repository
```bash
git clone <repository-url>
cd pet-management
```

### 2. Create Virtual Environment
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Database Setup

#### Option A: Using SQL Script
```bash
# Create MySQL database
mysql -u root -p
CREATE DATABASE pet_management;
exit

# Import the schema
mysql -u root -p pet_management < create_tables.sql
```

#### Option B: Using Flask-Migrate
```bash
# Initialize migration repository
flask db init

# Create initial migration
flask db migrate -m "Initial migration"

# Apply migration
flask db upgrade
```

### 5. Environment Configuration
```bash
# Copy environment template
cp env_example.txt .env

# Edit .env file with your database credentials
# Update DATABASE_URL with your MySQL connection details
```

### 6. Run the Application
```bash
# Method 1: Using Flask CLI
flask run

# Method 2: Using Python
python run.py
```

The application will be available at `http://localhost:5000`

## Default Login Credentials

### Admin Account
- **Username**: admin
- **Password**: password123

### Employee Account
- **Username**: employee1
- **Password**: password123

## Project Structure

```
pet-management/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── models.py            # Database models
│   ├── routes_auth.py       # Authentication routes
│   ├── routes_admin.py      # Admin routes
│   ├── routes_employee.py   # Employee routes
│   └── templates/
│       ├── base.html       # Base template
│       ├── auth/           # Authentication templates
│       ├── admin/          # Admin templates
│       └── employee/       # Employee templates
├── create_tables.sql       # Database schema
├── requirements.txt        # Python dependencies
├── env_example.txt        # Environment variables template
├── run.py                 # Application entry point
└── README.md             # This file
```

## API Endpoints

### Authentication
- `POST /login` - User login
- `POST /register` - User registration
- `GET /logout` - User logout

### Admin Routes
- `GET /admin/dashboard` - Admin dashboard
- `GET /admin/pets` - List all pets
- `POST /admin/pets/create` - Create new pet
- `GET /admin/pets/<id>` - Pet details
- `PUT /admin/pets/<id>/edit` - Edit pet
- `DELETE /admin/pets/<id>/delete` - Delete pet
- `GET /admin/donations` - List donations
- `POST /admin/donations/create` - Create donation
- `GET /admin/adoptions` - List adoptions
- `POST /admin/adoptions/create` - Create adoption
- `GET /admin/medical-records` - List medical records
- `POST /admin/medical-records/create` - Create medical record

### Employee Routes
- `GET /employee/dashboard` - Employee dashboard
- `GET /employee/pets` - View pets (read-only)
- `GET /employee/pets/<id>` - Pet details
- `POST /employee/donate` - Create donation
- `GET /employee/adopt` - Available pets for adoption
- `POST /employee/adopt/<id>` - Adopt pet
- `GET /employee/medical-records` - View medical records
- `GET /employee/my-donations` - Employee's donations
- `GET /employee/my-adoptions` - Employee's adoptions

## Database Schema

### Tables
- **users**: User authentication and roles
- **pets**: Pet information and status
- **donations**: Financial contributions
- **adoptions**: Pet adoption records
- **medical_records**: Pet medical history

### Key Relationships
- Users can have multiple donations and adoptions
- Pets can have multiple medical records and adoptions
- Donations can be linked to medical records
- Foreign key constraints ensure data integrity

## Testing

### Running Tests
```bash
# Install test dependencies
pip install pytest

# Run tests
pytest tests/
```

### Test Coverage
- Authentication and authorization
- CRUD operations for all entities
- Role-based access control
- Form validation
- API endpoints

## Development

### Adding New Features
1. Create database models in `app/models.py`
2. Add routes in appropriate blueprint files
3. Create HTML templates in `app/templates/`
4. Update navigation in `base.html`

### Database Migrations
```bash
# Create new migration
flask db migrate -m "Description of changes"

# Apply migration
flask db upgrade
```

## Deployment

### Production Considerations
1. Change `SECRET_KEY` in production
2. Use environment variables for database credentials
3. Set `FLASK_ENV=production`
4. Use a production WSGI server (e.g., Gunicorn)
5. Configure reverse proxy (e.g., Nginx)
6. Set up SSL certificates
7. Regular database backups

### Docker Deployment (Optional)
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "run:app"]
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions, please open an issue in the repository.

## Changelog

### Version 1.0.0
- Initial release
- Complete CRUD functionality
- Role-based authentication
- Responsive web interface
- MySQL database integration
