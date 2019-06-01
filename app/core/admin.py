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