# Pet Management System

A comprehensive web application for managing pet adoptions, donations, and medical records built with Flask, MySQL, and Bootstrap.

## Features

### Authentication & Roles
- **Admin Role**: Full CRUD access to all system data
- **Employee Role**: Limited access to create/update their own donations and adoptions
- Secure password hashing with Flask-Login
- Role-based route protection

### Pet Management
- Add, edit, and delete pet records
- Track pet status (available, adopted, foster)
- Upload pet images via URL
- Comprehensive pet information including breed, age, gender

### Donation System
- Record financial contributions
- Link donations to medical treatments
- Track donor information
- Employee-specific donation tracking

### Adoption Process
- Manage pet adoptions
- Track adopter information
- Automatic pet status updates
- Employee adoption management

### Medical Records
- Track pet medical treatments
- Link treatments to donations
- Vaccine tracking
- Treatment history

## Technology Stack

- **Backend**: Flask
- **Database**: MySQL
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Authentication**: Flask-Login
- **ORM**: SQL
- **Database Migration**: Flask
  

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

## Development

### Adding New Features
1. Create database models in `app/models.py`
2. Add routes in appropriate blueprint files
3. Create HTML templates in `app/templates/`
4. Update navigation in `base.html`


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
