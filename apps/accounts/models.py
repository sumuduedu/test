from django.contrib.auth.models import AbstractUser
from django.db import models


class UserRole(models.TextChoices):
    ADMIN = 'admin', 'Admin'
    STAFF = 'staff', 'Staff'
    TEACHER = 'teacher', 'Teacher'
    STUDENT = 'student', 'Student'
    PARENT = 'parent', 'Parent'
    ALUMNI = 'alumni', 'Alumni'


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=UserRole.choices, default=UserRole.STUDENT)
    is_active = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=20, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.email} ({self.get_role_display()})'
