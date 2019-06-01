from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from core import models

class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['email', 'username']


admin.site.register(models.User, UserAdmin)
admin.site.register(models.Module)
admin.site.register(models.Lesson)
admin.site.register(models.Lecturer)
admin.site.register(models.Board)
admin.site.register(models.Location)
admin.site.register(models.Caption)
admin.site.register(models.Comment)
admin.site.register(models.Pillar)
admin.site.register(models.CohortClass)
admin.site.register(models.LessonType)


"""Create model Caption
    - Create model LessonType
    - Create model Pillar
    - Remove field id from board
    - Add field duration to lesson
    - Alter field type on lesson
    - Create model Comment
    - Create model CohortClass
    - Add field caption to board
    - Add field class_group to lesson"""