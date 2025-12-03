import json
import pytest


class TestUserRoutes:
    """Test user-related endpoints"""

    def test_get_profile(self, client, test_user):
        """Test getting user profile"""
        # Login first to get token
        login_response = client.post('/api/auth/login',
                                      data=json.dumps({
                                          'username_or_email': 'testuser',
                                          'password': 'TestPass123'
                                      }),
                                      content_type='application/json')

        token = json.loads(login_response.data)['access_token']

        # Get profile
        response = client.get('/api/users/profile',
                             headers={'Authorization': f'Bearer {token}'})

        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'user' in data
        assert data['user']['username'] == 'testuser'

    def test_update_profile(self, client, test_user):
        """Test updating user profile"""
        # Login first to get token
        login_response = client.post('/api/auth/login',
                                      data=json.dumps({
                                          'username_or_email': 'testuser',
                                          'password': 'TestPass123'
                                      }),
                                      content_type='application/json')

        token = json.loads(login_response.data)['access_token']

        # Update profile
        response = client.put('/api/users/profile',
                             data=json.dumps({
                                 'first_name': 'Updated',
                                 'last_name': 'Name'
                             }),
                             headers={'Authorization': f'Bearer {token}'},
                             content_type='application/json')

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['user']['first_name'] == 'Updated'
        assert data['user']['last_name'] == 'Name'

    def test_get_user_by_id(self, client, test_user):
        """Test getting user by ID (public info)"""
        response = client.get(f'/api/users/{test_user.id}')

        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'user' in data
        assert data['user']['username'] == 'testuser'
        # Email should not be included for public access
        assert 'email' not in data['user'] or data['user']['email'] is None

    def test_get_nonexistent_user(self, client):
        """Test getting nonexistent user"""
        response = client.get('/api/users/99999')

        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'error' in data
