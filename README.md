# Cap Shop

An e-commerce application for selling caps with user authentication and order management.

## Features

- User registration and authentication
- JWT-based token authentication
- Secure password hashing with bcrypt
- User profile management
- Order history tracking (coming soon)
- RESTful API design

## Tech Stack

### Backend
- **Flask** - Python web framework
- **Flask-SQLAlchemy** - ORM for database operations
- **Flask-JWT-Extended** - JWT authentication
- **Flask-Bcrypt** - Password hashing
- **SQLite** - Database (easily upgradable to PostgreSQL)
- **pytest** - Testing framework

## Project Structure

```
cap_shop/
├── backend/
│   ├── app/
│   │   ├── __init__.py          # App factory and initialization
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   └── user.py          # User model
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── auth_routes.py   # Authentication endpoints
│   │   │   └── user_routes.py   # User management endpoints
│   │   ├── middleware/
│   │   │   └── __init__.py
│   │   └── utils/
│   │       └── validators.py    # Input validation functions
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── conftest.py          # Test fixtures
│   │   ├── test_auth.py         # Authentication tests
│   │   └── test_user_routes.py  # User routes tests
│   ├── config.py                # Configuration settings
│   ├── run.py                   # Application entry point
│   ├── requirements.txt         # Python dependencies
│   ├── .env.example            # Environment variables template
│   └── .gitignore
├── frontend/                    # (To be implemented)
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.8+
- pip (Python package manager)
- virtualenv (recommended)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/gumruyanzh/cap_shop.git
cd cap_shop
```

2. Set up virtual environment:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env and set your secret keys
```

5. Run the application:
```bash
python run.py
```

The API will be available at `http://localhost:5000`

### Running Tests

```bash
# From the backend directory
pytest

# Run with coverage
pytest --cov=app tests/

# Run specific test file
pytest tests/test_auth.py

# Run with verbose output
pytest -v
```

## API Endpoints

### Authentication

#### Register a new user
```http
POST /api/auth/register
Content-Type: application/json

{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "SecurePass123",
  "first_name": "John",
  "last_name": "Doe"
}
```

**Response (201 Created):**
```json
{
  "message": "User registered successfully",
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "is_active": true,
    "created_at": "2025-12-03T12:00:00",
    "updated_at": "2025-12-03T12:00:00"
  },
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

#### Login
```http
POST /api/auth/login
Content-Type: application/json

{
  "username_or_email": "johndoe",
  "password": "SecurePass123"
}
```

**Response (200 OK):**
```json
{
  "message": "Login successful",
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "is_active": true,
    "created_at": "2025-12-03T12:00:00",
    "updated_at": "2025-12-03T12:00:00"
  },
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

#### Refresh Token
```http
POST /api/auth/refresh
Authorization: Bearer <refresh_token>
```

**Response (200 OK):**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

#### Get Current User
```http
GET /api/auth/me
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "is_active": true,
    "created_at": "2025-12-03T12:00:00",
    "updated_at": "2025-12-03T12:00:00"
  }
}
```

### User Management

#### Get Profile
```http
GET /api/users/profile
Authorization: Bearer <access_token>
```

#### Update Profile
```http
PUT /api/users/profile
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "first_name": "John",
  "last_name": "Smith",
  "email": "john.smith@example.com"
}
```

#### Get User by ID
```http
GET /api/users/{user_id}
```

### Health Check
```http
GET /api/health
```

**Response (200 OK):**
```json
{
  "status": "healthy",
  "message": "Cap Shop API is running"
}
```

## Password Requirements

- Minimum 8 characters
- At least one uppercase letter
- At least one lowercase letter
- At least one digit

## Username Requirements

- 3-80 characters
- Alphanumeric and underscores only

## Security Features

- Password hashing using bcrypt
- JWT token-based authentication
- Access tokens expire after 1 hour
- Refresh tokens expire after 30 days
- Input validation and sanitization
- SQL injection protection via SQLAlchemy ORM
- CORS support for frontend integration

## Environment Variables

Required environment variables (see `.env.example`):

- `FLASK_APP` - Application entry point
- `FLASK_ENV` - Environment (development/testing/production)
- `SECRET_KEY` - Flask secret key
- `JWT_SECRET_KEY` - JWT signing key
- `DATABASE_URL` - Database connection string

## Testing

The test suite includes:

- User registration tests
- Login authentication tests
- Password validation tests
- Email validation tests
- Duplicate username/email detection
- Protected endpoint access tests
- Token refresh tests
- Profile management tests

## Future Enhancements

- Product catalog management
- Shopping cart functionality
- Order processing and history
- Payment integration
- Admin dashboard
- Email verification
- Password reset functionality
- Social authentication
- Rate limiting
- API documentation with Swagger/OpenAPI

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/CLCE-X-description`)
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## License

This project is licensed under the MIT License.

## Issue Tracking

Issues are tracked using the CLCE prefix (e.g., CLCE-2 for user login functionality).