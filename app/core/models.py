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


class Lecturer(models.Model):
    """Lecturer model for for every board will be assigned to a lecturer"""
    name = models.CharField(max_length=255)
    #  Link the user to the lecturer model
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE)

    lessons = models.ManyToManyField("Lesson")

    def __str__(self):
        return self.name

class Pillar(models.Model):
    abbr = models.CharField(max_length=10)
    name = models.CharField(max_length=50)

class LessonType(models.Model):
    name = models.CharField(max_length=30, default = None)

    def __str__(self):
        return self.name


class CohortClass(models.Model):
    pillar = models.ForeignKey(Pillar, on_delete=models.PROTECT)
    name = models.CharField(max_length=50, blank=True, default='')
    number = models.IntegerField()

    def __str__(self):
        return f"Pillar: {pillar} {name} Class {number}"

class Lesson(models.Model):

    """TODO: include duration, class and include type as one of the model"""

    # Lecture/ Lab/ Cohort
    type = models.ForeignKey(LessonType, on_delete=models.PROTECT)
    # over = models.BooleanField(default=False)
    module = models.ForeignKey(Module, on_delete=models.PROTECT)
    location = models.ForeignKey(Location, on_delete=models.PROTECT)
    lesson_time = models.DateTimeField(default=None)
    duration = models.DateTimeField(default=None)
    class_group = models.ForeignKey(CohortClass, default=None, on_delete=models.CASCADE)
    # lecturer = models.ForeignKey(Lecturer, on_delete=models.PROTECT, default = None)


    def __str__(self):
        return self.module.__str__() + ": " + type


"""TODO: Fix the weird one to one relationship between caption and board. Try and figure out what is happening 
under th"""
class Caption(models.Model):
    caption_id = models.AutoField(default=None, primary_key=True)
    caption_text = models.CharField(max_length = 140, default=None)

    def __str__(self):
        return caption_text

class Board(models.Model):
    """Boards model"""

    image_url = models.CharField(max_length=255)
    # TODO: check if I need to set delete as cascade
    lesson = models.ForeignKey(Lesson, on_delete=models.PROTECT)
    text_on_board = models.CharField(max_length=3000)
    time_taken = models.DateTimeField()
    # caption = models.ForeignKey(Caption, on_delete=models.CASCADE, default=None)
    caption = models.OneToOneField(Caption, to_field = 'caption_id', primary_key= True, related_name= 'board', on_delete=models.CASCADE, default = None)

class Comment(models.Model):
    comment_text = models.CharField(max_length=3000)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)

    def __str__(self):
        return self.comment_text







# class CommentVote(models.Model):
#
#
# class Star(models.Model):





