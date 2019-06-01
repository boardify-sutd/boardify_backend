from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Module

from boards.serializers import ModuleSerializer

MODULES_URL = reverse('boards:module-list')

def create_user(**params):
    return get_user_model().objects.create_user(**params)

class PublicModulesApiTests(TestCase):
    """Test the publicly available modules API"""

    def setUp(self):
        self.client = APIClient()


    def test_login_required(self):
        """Test that login is required for retrieving tags"""

        res = self.client.get(MODULES_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagsApiTests(TestCase):

    def setUp(self):
        self.user = create_user(email="lionellloh@gmail.com",
                                password="password123",
                                username="name")

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_modules(self):
        """Test that an authenticated user can retrieve tags"""

        Module.objects.create(user=self.user, name="Physics")
        Module.objects.create(user=self.user, name="Chemistry")

        res = self.client.get(MODULES_URL)
        modules = Module.objects.all().order_by('-name')

        serializer = ModuleSerializer(modules, many = True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_module_successful(self):
        """Test creating a new module"""
        payload = {'name': 'Test Module'}
        self.client.post(MODULES_URL, payload)

        exists = Module.objects.filter(
            user=self.user,
            name=payload['name']
        ).exists()

        self.assertTrue(exists)

    def test_create_module_invalid(self):
        """Test creating a new module with invalid payload"""
        payload = {'name': ''}
        res = self.client.post(MODULES_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)