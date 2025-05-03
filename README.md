

# Medical Appointment System - Backend API

A RESTful API for managing medical appointments, patient records, and hospital-doctor relationships.

## Project Structure

```
/backend
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── extensions.py
│   ├── routes/
│   ├── models/
│   ├── services/
│   └── utils/
├── migrations/
├── .env
├── requirements.txt
└── wsgi.py
/frontend
```

## Prerequisites

- Python 3.10+
- PostgreSQL 14+
- pipenv (recommended)
- Postman (for API testing)

## Setup Instructions

### 1. Clone Repository
```bash
git clone https://github.com/Posa5A6/PMDCS
cd PMDCS
```

### 2. Create env and activate
```
virtualenv env
source env/bin/activate # linux
env/scripts/activate #windows
```


### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configuration
Create `.env` file:
```env
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret
DATABASE_URL=postgresql://postgres:password@localhost:5432/medapp
CORS_ORIGINS=http://localhost:3000
```

### 5. Database Setup
```bash
# Create database
createdb pmdcs

# Initialize migrations
flask db init
flask db migrate
flask db upgrade
```

### 6. Run Server
```bash
flask run --host=0.0.0.0 --port=5000
# Or for production:
gunicorn --bind 0.0.0.0:5000 wsgi:app
```

## API Documentation

### Authentication

| Method | Endpoint          | Description          | Required Role |
|--------|-------------------|----------------------|---------------|
| POST   | /api/auth/register| User registration    | None          |
| POST   | /api/auth/login   | User login           | None          |
| POST   | /api/auth/refresh | Refresh JWT token    | Authenticated |
| GET    | /api/auth/profile | Get user profile     | Authenticated |

**Sample Login Request:**
```json
{
  "username":"doc",
  "email": "doctor@hospital.com",
  "password": "SecurePassword123!",
  "role":"doctor"
}
```

### Users

| Method | Endpoint          | Description          | Required Role |
|--------|-------------------|----------------------|---------------|
| GET    | /api/users/{id}   | Get user by ID       | Admin         |
| PUT    | /api/users/{id}   | Update user          | Admin         |

### Hospitals

| Method | Endpoint          | Description          | Required Role |
|--------|-------------------|----------------------|---------------|
| GET    | /api/hospitals    | List all hospitals   | Authenticated |
| POST   | /api/hospitals    | Create new hospital  | Admin         |

### Appointments

| Method | Endpoint          | Description          | Required Role |
|--------|-------------------|----------------------|---------------|
| GET    | /api/appointments | List appointments    | All Roles     |
| POST   | /api/appointments | Create appointment   | Patient       |
| PUT    | /api/appointments/{id} | Update appointment | Doctor/Admin |
| GET    | /api/appointments/{id} | Get appointment | Authenticated |

**Sample Appointment Creation:**
```json
{
  "doctor_id": 2,
  "hospital_id": 1,
  "appointment_date": "2024-03-20T14:30:00Z",
  "purpose": "Annual checkup"
}
```

### Patient Records

| Method | Endpoint          | Description          | Required Role |
|--------|-------------------|----------------------|---------------|
| GET    | /api/patient-records | List all records | Doctor/Admin |

## Testing with Postman

1. Import [Postman Collection](link-to-collection)
2. Set environment variables:
   - `base_url`: http://localhost:5000/api
   - `token`: (set after login)

**Example Flow:**
1. Register user → POST /auth/register
2. Login → POST /auth/login
3. Create appointment → POST /appointments
4. View appointments → GET /appointments

## Troubleshooting

**Common Issues:**
- **Database Connection Failed**: Verify PostgreSQL is running and DATABASE_URL is correct
- **Migration Errors**: Try:
  ```bash
  rm -rf migrations/
  flask db init
  flask db migrate
  flask db upgrade
  ```
- **JWT Errors**: Check token expiration and secret keys
- **CORS Errors**: Verify CORS_ORIGINS in .env matches frontend URL

