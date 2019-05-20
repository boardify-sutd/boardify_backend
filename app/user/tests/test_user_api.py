from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')

def create_user(**params):
    return get_user_model().objects.create_user(**params)

class PublicUserApiTests(TestCase):
    """Test the users API (public) """

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test creating user with valid credentials is successful"""

        credentials = {
            'email': 'lionellloh@xmail.com',
            'password': 'lionellloh',
            'name': 'test name'
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
            'name': 'test name'
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