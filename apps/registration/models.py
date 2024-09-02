from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    USER_TYPES = (
        ('student', 'Student'),
        ('account_manager', 'Account Manager'),
        ('teacher', 'Teacher'),
        ('super_admin', 'Super Admin'),        
    )

    user_type = models.CharField(max_length=50, choices=USER_TYPES, default='student')

    def __str__(self):
        return self.username
    

    