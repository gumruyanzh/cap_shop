import json
import pytest
from app.models.user import User


class TestRegistration:
    """Test user registration endpoint"""

    def test_successful_registration(self, client):
        """Test successful user registration"""
        response = client.post('/api/auth/register',
                               data=json.dumps({
                                   'username': 'newuser',
                                   'email': 'newuser@example.com',
                                   'password': 'SecurePass123',
                                   'first_name': 'New',
                                   'last_name': 'User'
                               }),
                               content_type='application/json')

        assert response.status_code == 201
        data = json.loads(response.data)
        assert 'user' in data
        assert 'access_token' in data
        assert 'refresh_token' in data
        assert data['user']['username'] == 'newuser'
        assert data['user']['email'] == 'newuser@example.com'

    def test_registration_missing_username(self, client):
        """Test registration fails without username"""
        response = client.post('/api/auth/register',
                               data=json.dumps({
                                   'email': 'test@example.com',
                                   'password': 'SecurePass123'
                               }),
                               content_type='application/json')

        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data

    def test_registration_missing_email(self, client):
        """Test registration fails without email"""
        response = client.post('/api/auth/register',
                               data=json.dumps({
                                   'username': 'testuser',
                                   'password': 'SecurePass123'
                               }),
                               content_type='application/json')

        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data

    def test_registration_missing_password(self, client):
        """Test registration fails without password"""
        response = client.post('/api/auth/register',
                               data=json.dumps({
                                   'username': 'testuser',
                                   'email': 'test@example.com'
                               }),
                               content_type='application/json')

        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data

    def test_registration_weak_password(self, client):
        """Test registration fails with weak password"""
        response = client.post('/api/auth/register',
                               data=json.dumps({
                                   'username': 'testuser',
                                   'email': 'test@example.com',
                                   'password': 'weak'
                               }),
                               content_type='application/json')

        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data

    def test_registration_invalid_email(self, client):
        """Test registration fails with invalid email"""
        response = client.post('/api/auth/register',
                               data=json.dumps({
                                   'username': 'testuser',
                                   'email': 'invalid-email',
                                   'password': 'SecurePass123'
                               }),
                               content_type='application/json')

        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data

    def test_registration_duplicate_username(self, client, test_user):
        """Test registration fails with duplicate username"""
        response = client.post('/api/auth/register',
                               data=json.dumps({
                                   'username': 'testuser',
                                   'email': 'different@example.com',
                                   'password': 'SecurePass123'
                               }),
                               content_type='application/json')

        assert response.status_code == 409
        data = json.loads(response.data)
        assert 'error' in data

    def test_registration_duplicate_email(self, client, test_user):
        """Test registration fails with duplicate email"""
        response = client.post('/api/auth/register',
                               data=json.dumps({
                                   'username': 'differentuser',
                                   'email': 'test@example.com',
                                   'password': 'SecurePass123'
                               }),
                               content_type='application/json')

        assert response.status_code == 409
        data = json.loads(response.data)
        assert 'error' in data


class TestLogin:
    """Test user login endpoint"""

    def test_successful_login_with_username(self, client, test_user):
        """Test successful login with username"""
        response = client.post('/api/auth/login',
                               data=json.dumps({
                                   'username_or_email': 'testuser',
                                   'password': 'TestPass123'
                               }),
                               content_type='application/json')

        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'user' in data
        assert 'access_token' in data
        assert 'refresh_token' in data
        assert data['message'] == 'Login successful'

    def test_successful_login_with_email(self, client, test_user):
        """Test successful login with email"""
        response = client.post('/api/auth/login',
                               data=json.dumps({
                                   'username_or_email': 'test@example.com',
                                   'password': 'TestPass123'
                               }),
                               content_type='application/json')

        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'user' in data
        assert 'access_token' in data
        assert 'refresh_token' in data

    def test_login_invalid_credentials(self, client, test_user):
        """Test login fails with invalid credentials"""
        response = client.post('/api/auth/login',
                               data=json.dumps({
                                   'username_or_email': 'testuser',
                                   'password': 'WrongPassword123'
                               }),
                               content_type='application/json')

        assert response.status_code == 401
        data = json.loads(response.data)
        assert 'error' in data

    def test_login_nonexistent_user(self, client):
        """Test login fails with nonexistent user"""
        response = client.post('/api/auth/login',
                               data=json.dumps({
                                   'username_or_email': 'nonexistent',
                                   'password': 'TestPass123'
                               }),
                               content_type='application/json')

        assert response.status_code == 401
        data = json.loads(response.data)
        assert 'error' in data

    def test_login_missing_credentials(self, client):
        """Test login fails without credentials"""
        response = client.post('/api/auth/login',
                               data=json.dumps({}),
                               content_type='application/json')

        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data


class TestProtectedEndpoints:
    """Test protected endpoints requiring authentication"""

    def test_get_current_user_with_valid_token(self, client, test_user):
        """Test getting current user with valid token"""
        # First login to get token
        login_response = client.post('/api/auth/login',
                                      data=json.dumps({
                                          'username_or_email': 'testuser',
                                          'password': 'TestPass123'
                                      }),
                                      content_type='application/json')

        token = json.loads(login_response.data)['access_token']

        # Then access protected endpoint
        response = client.get('/api/auth/me',
                             headers={'Authorization': f'Bearer {token}'})

        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'user' in data
        assert data['user']['username'] == 'testuser'

    def test_get_current_user_without_token(self, client):
        """Test accessing protected endpoint without token fails"""
        response = client.get('/api/auth/me')

        assert response.status_code == 401

    def test_refresh_token(self, client, test_user):
        """Test refreshing access token"""
        # First login to get refresh token
        login_response = client.post('/api/auth/login',
                                      data=json.dumps({
                                          'username_or_email': 'testuser',
                                          'password': 'TestPass123'
                                      }),
                                      content_type='application/json')

        refresh_token = json.loads(login_response.data)['refresh_token']

        # Use refresh token to get new access token
        response = client.post('/api/auth/refresh',
                              headers={'Authorization': f'Bearer {refresh_token}'})

        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'access_token' in data
