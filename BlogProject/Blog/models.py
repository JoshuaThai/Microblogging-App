from django.db import models

# Create your models here.

class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=320)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    birthDate = models.DateField(auto_now= False, auto_now_add=False)
    accountCreated = models.DateTimeField(auto_now_add=True) # set the time to now when object is first created.

    ROLE_CHOICES = (
        ('user', 'User'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=100, choices=ROLE_CHOICES, default='user') # Can be user of admin
