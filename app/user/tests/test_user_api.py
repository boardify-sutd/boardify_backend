from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:register')
TOKEN_URL = reverse('user:login')
ME_URL = reverse('user:self')

def create_user(**params):
    return get_user_model().objects.create_user(**params)

class PublicUserApiTests(TestCase):
    """Test the users API (public) """

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test if creating user with valid credentials is successful"""

        credentials = {
            'email': 'lionellloh@xmail.com',
            'password': 'lionellloh',
            'username': 'test name'
        }

        res = self.client.post(CREATE_USER_URL, credentials)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(credentials['password']))
        self.assertNotIn('password', res.data)


    def test_create_existing_user(self):
        """Test creating a user that already exists fails"""

        credentials = {
            'email': 'lionellloh@xmail.com',
            'password': 'lionellloh',
            'username': 'test name'
        }

        create_user(**credentials)

        res = self.client.post(CREATE_USER_URL, credentials)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    #     Every test function resets the database, so even if we are reusing the credentials, it is ok.
    # def test_password_too_short(self):
    #     """Test that the password must be more than or equal to 6 characters"""
    #
    #     credentials = {
    #         'email': 'lionellloh@xmail.com',
    #         'password': '1234',
    #         'name': 'test name'
    #     }
    #
    #     res = self.client.post(CREATE_USER_URL, credentials)
    #
    #     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    #     user_exists = get_user_model().objects.filter(
    #         email=credentials["email"]
    #     ).exists()
    #     self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Test that a token is created for a user"""

        credentials = {
            'email': 'lionellloh@xmail.com',
            'password': 'lionellloh',
            'username': 'test name'
        }

        create_user(**credentials)
        res = self.client.post(TOKEN_URL, credentials)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """Test that token is not created if invalid credentials are given"""
        create_user(email="lionellloh@xmail.com", password="password123")

        credentials = {
            'email': 'lionellloh@xmail.com',
            'password': 'wrong',
            'username': 'test name'
        }

        res = self.client.post(TOKEN_URL, credentials)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


    def test_create_token_no_user(self):
        """Test that token is not created if user doesn't exist"""

        credentials = {
            'email': 'lionellloh@xmail.com',
            'password': 'wrong',
            'username': 'test name'
        }

        res = self.client.post(TOKEN_URL, credentials)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


    def test_create_token_missing_field(self):
        """Test that email and password are required"""

        res = self.client.post(TOKEN_URL, {'email': 'lionellloh@xmail.com', 'password': ''})
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


    def retrieve_user_unauthorised(self):
        """Test that authentication is required for user"""

        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)



class PrivateUserAPItests(TestCase):
    """Test API requests that require authentication"""

    def setUp(self):
        self.user = create_user(
            email = "lionellloh@gmail.com",
            password = "password123",
            username = "lionellloh")

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def retrieve_profile_success(self):
        """Test retrieving profile for logged in user"""
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'username': self.user.username,
            'email': self.user.email
        })

    def test_post_me_not_allowed(self):
        """Test that POST is not allowed for the ME endpoint"""
        res = self.client.post(ME_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


    def test_update_user_profile(self):
        """Test updating the profile for authenticated user"""

        payload = {'username' : 'lionellloh',
                   'password' : 'newpassword123'}

        res = self.client.patch(ME_URL, payload)
        self.user.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.username, payload['username'])
        self.assertTrue(self.user.check_password(payload['password']))









