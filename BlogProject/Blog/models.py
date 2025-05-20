from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class User(AbstractUser):
    birthDate = models.DateField(auto_now= False, auto_now_add=False, null=True, blank=True)
    accountCreated = models.DateTimeField(auto_now_add=True) # set the time to now when object is first created.

    ROLE_CHOICES = (
        ('user', 'User'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=100, choices=ROLE_CHOICES, default='user') # Can be user of admin
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
