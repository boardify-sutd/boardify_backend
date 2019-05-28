from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

from django.conf import settings

# Create your models here.

class UserManager(BaseUserManager):

    def create_user(self, email, password = None, **extra_fields):
        """Creates and saves a new user. Returns the user object."""
        # Validation
        if not email:
            raise ValueError("User must have an email address")

        user = self.model(email = email.lower(), **extra_fields)
        user.set_password(password)
        user.save(using = self._db)

        return user

    def create_superuser(self, email, password):
        """Creates and saves a new super user. Return the super user instance"""

        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True

        user.save(using=self._db)

        return user

class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username"""

    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"


class Module(models.Model):
    """A Module is a subject that every board will have"""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name


class Location(models.Model):
    """Location model that every board will be tagged to based on where the lesson was held"""

    code = models.CharField(max_length=255)
    name = models.CharField(max_length=255)


    def __str__(self):
        return self.code


    def getName(self):
        return self.name




