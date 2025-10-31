# Pet Management System - API Documentation

## Overview

The Pet Management System provides a RESTful API for managing pets, donations, adoptions, and medical records. The API supports both JSON responses and HTML templates.

## Base URL
```
http://localhost:5000
```

## Authentication

All API endpoints require authentication except for login and registration.

### Login
```http
POST /login
Content-Type: application/x-www-form-urlencoded

username=admin&password=password123
```

**Response:**
```json
{
  "success": true,
  "redirect": "/admin/dashboard",
  "role": "admin"
}
```

### Registration
```http
POST /register
Content-Type: application/x-www-form-urlencoded

username=newuser&email=newuser@example.com&password=password123&confirm_password=password123&role=employee
```

**Response:**
```json
{
  "success": true,
  "message": "User created successfully"
}
```

## Admin Endpoints

### Dashboard
```http
GET /admin/dashboard
```

Returns admin dashboard with statistics and recent activities.

### Pets Management

#### List All Pets
```http
GET /admin/pets
```

#### Create Pet
```http
POST /admin/pets/create
Content-Type: application/x-www-form-urlencoded

pet_name=Buddy&breed=Golden Retriever&age=3&gender=male&status=available&description=Friendly dog&img_url=https://example.com/image.jpg&shelter_no=SH001
```

**Response:**
```json
{
  "success": true,
  "pet_id": 1
}
```

#### Get Pet Details
```http
GET /admin/pets/{pet_id}
```

#### Update Pet
```http
POST /admin/pets/{pet_id}/edit
Content-Type: application/x-www-form-urlencoded

pet_name=Buddy Updated&breed=Golden Retriever&age=4&gender=male&status=available
```

#### Delete Pet
```http
POST /admin/pets/{pet_id}/delete
```

### Donations Management

#### List All Donations
```http
GET /admin/donations
```

#### Create Donation
```http
POST /admin/donations/create
Content-Type: application/x-www-form-urlencoded

amount=100.00&purpose=Medical care&donor_name=John Doe&donor_email=john@example.com&donor_phone=+1234567890&message=Hope this helps
```

### Adoptions Management

#### List All Adoptions
```http
GET /admin/adoptions
```

#### Create Adoption
```http
POST /admin/adoptions/create
Content-Type: application/x-www-form-urlencoded

adopt_name=Jane Smith&adopt_email=jane@example.com&adopt_phone=+1987654321&pet_id=1&address=123 Main St
```

### Medical Records Management

#### List All Medical Records
```http
GET /admin/medical-records
```

#### Create Medical Record
```http
POST /admin/medical-records/create
Content-Type: application/x-www-form-urlencoded

pet_id=1&treatment_type=Vaccination&treat_date=2024-01-15&donor_id=1&vaccines=Rabies, DHPP&description=Annual vaccination
```

## Employee Endpoints

### Dashboard
```http
GET /employee/dashboard
```

Returns employee dashboard with limited statistics.

### View Pets
```http
GET /employee/pets
```

#### Get Pet Details
```http
GET /employee/pets/{pet_id}
```

### Donations

#### Create Donation
```http
POST /employee/donate
Content-Type: application/x-www-form-urlencoded

amount=50.00&purpose=General care&donor_name=Employee Name&donor_email=employee@example.com&donor_phone=+1234567890&message=Happy to help
```

#### View Own Donations
```http
GET /employee/my-donations
```

#### Edit Own Donation
```http
POST /employee/my-donations/{donation_id}/edit
Content-Type: application/x-www-form-urlencoded

amount=75.00&purpose=Updated purpose&donor_name=Updated Name&donor_email=updated@example.com
```

### Adoptions

#### List Available Pets for Adoption
```http
GET /employee/adopt
```

#### Adopt Pet
```http
POST /employee/adopt/{pet_id}
Content-Type: application/x-www-form-urlencoded

adopt_name=Adopter Name&adopt_email=adopter@example.com&adopt_phone=+1234567890&address=123 Main St
```

#### View Own Adoptions
```http
GET /employee/my-adoptions
```

#### Edit Own Adoption
```http
POST /employee/my-adoptions/{adoption_id}/edit
Content-Type: application/x-www-form-urlencoded

adopt_name=Updated Name&adopt_email=updated@example.com&adopt_phone=+1234567890&address=Updated Address
```

### Medical Records

#### View Medical Records
```http
GET /employee/medical-records
```

## Error Responses

### Validation Errors
```json
{
  "error": "Pet name is required"
}
```

### Multiple Validation Errors
```json
{
  "errors": [
    "Username must be at least 3 characters long",
    "Valid email is required"
  ]
}
```

### Authentication Errors
```json
{
  "error": "Invalid username or password"
}
```

### Authorization Errors
```json
{
  "error": "Admin access required"
}
```

## Data Models

### User
```json
{
  "id": 1,
  "username": "admin",
  "email": "admin@example.com",
  "role": "admin",
  "created_at": "2024-01-01T00:00:00Z"
}
```

### Pet
```json
{
  "pet_id": 1,
  "pet_name": "Buddy",
  "breed": "Golden Retriever",
  "age": 3,
  "gender": "male",
  "status": "available",
  "description": "Friendly dog",
  "img_url": "https://example.com/image.jpg",
  "shelter_no": "SH001",
  "created_at": "2024-01-01T00:00:00Z"
}
```

### Donation
```json
{
  "id": 1,
  "amount": 100.50,
  "purpose": "Medical care",
  "donor_name": "John Doe",
  "donor_email": "john@example.com",
  "donor_phone": "+1234567890",
  "message": "Hope this helps",
  "date": "2024-01-01T00:00:00Z",
  "user_id": 1
}
```

### Adoption
```json
{
  "id": 1,
  "adopt_name": "Jane Smith",
  "adopt_email": "jane@example.com",
  "adopt_phone": "+1987654321",
  "pet_id": 1,
  "date": "2024-01-01T00:00:00Z",
  "address": "123 Main St",
  "user_id": 1
}
```

### Medical Record
```json
{
  "id": 1,
  "pet_id": 1,
  "treatment_type": "Vaccination",
  "treat_date": "2024-01-15",
  "donor_id": 1,
  "vaccines": "Rabies, DHPP",
  "description": "Annual vaccination",
  "created_at": "2024-01-01T00:00:00Z"
}
```

## Status Codes

- `200` - Success
- `302` - Redirect (after successful form submission)
- `400` - Bad Request (validation errors)
- `401` - Unauthorized (invalid credentials)
- `403` - Forbidden (insufficient permissions)
- `404` - Not Found
- `500` - Internal Server Error

## Rate Limiting

Currently, no rate limiting is implemented. In production, consider implementing rate limiting for API endpoints.

## CORS

CORS is not configured. If you need to access the API from a different domain, configure CORS headers.

## Testing

### Using curl

#### Login
```bash
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=password123"
```

#### Create Pet (Admin)
```bash
curl -X POST http://localhost:5000/admin/pets/create \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "pet_name=Test Pet&breed=Test Breed&age=2&gender=male&status=available"
```

#### Create Donation (Employee)
```bash
curl -X POST http://localhost:5000/employee/donate \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "amount=50.00&donor_name=Test Donor&donor_email=test@example.com"
```

### Using Python requests

```python
import requests

# Login
response = requests.post('http://localhost:5000/login', data={
    'username': 'admin',
    'password': 'password123'
})

# Create pet
response = requests.post('http://localhost:5000/admin/pets/create', data={
    'pet_name': 'Test Pet',
    'breed': 'Test Breed',
    'age': 2,
    'gender': 'male',
    'status': 'available'
})
```

## Postman Collection

A Postman collection is available in the `postman/` directory with pre-configured requests for all API endpoints.

## Notes

- All timestamps are in UTC
- Decimal amounts are stored with 2 decimal places
- File uploads are not supported (only image URLs)
- The API returns both JSON and HTML responses depending on the request format
- Session-based authentication is used (cookies)
