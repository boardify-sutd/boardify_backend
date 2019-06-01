from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models

def sample_user(email="lionellloh@xmail.com", password="password123"):
    """Create a sample user"""

    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""

        email = "test@lionell.com"
        password = "testpass123"

        user = get_user_model().objects.create_user(
            email = email,
            password = password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))


    def test_new_user_email_normalized(self):
        """Test that the email for a new user is normalized (domain reduced to lower case)"""
        email = "liOnelL@gmail.com"
        user = get_user_model().objects.create_user(email, "test123")

        self.assertEqual(user.email, email.lower())

    def test_new_user_null_email(self):
        """Test creating user with no email raises error"""

        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, "lionell123")


    def test_create_new_super_user(self):
        """Test the creation of new super user"""

        user = get_user_model().objects.create_superuser(
            'lionellloh@gmail.com',
            'lalala123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)


    def test_module_str(self):
        """Test the creation of modules"""

        module = models.Module.objects.create(
            user=sample_user(),
            name="Physics"
        )

        self.assertEqual(module.name, "Physics")


    def test_location_str(self):
        """Test the creation of locations"""

        location = models.Location.objects.create(
            code="2.505",
            name="Lecture Theatre 3"

        )

        self.assertEqual(location.code, "2.505")
        self.assertEqual(location.name, "Lecture Theatre 3")


    def test_lecturer_str(self):
        """Test the creation of lectuer"""

        lecturer = models.Lecturer.objects.create(
            user=sample_user(),
            name="David Yeow"
        )

        self.assertEqual(lecturer.name, "David Yeow")










