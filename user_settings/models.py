from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    # Probably better to change the user id according to the following link
    #
    # http://stackoverflow.com/questions/2672975/django-biginteger-auto-increment-field-as-primary-key
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=200)
    gender = models.CharField(max_length=20)
    date_registration = models.DateTimeField()
