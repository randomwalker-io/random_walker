from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    gender_choice = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('', 'Unspecified'),
    )
    gender = models.CharField(max_length=2, choices = gender_choice, default='')
