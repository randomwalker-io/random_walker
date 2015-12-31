from django.db import models

# Create your models here.
class User(models.Model):
    # Probably better to change the user id according to the following link
    #
    # http://stackoverflow.com/questions/2672975/django-biginteger-auto-increment-field-as-primary-key
    user_id = models.BigIntegerField()
    user_first_name = models.CharField(max_length=200)
    user_last_name = models.CharField(max_length=200)
    user_email = models.CharField(max_length=200)
    user_address = models.CharField(max_length=200)
    user_gender = models.CharField(max_length=20)
    password_salt = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    user_date_registration = models.DateTimeField()
    

class Location(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    origin_lat = models.DecimalField(max_digits=20, decimal_places=10)
    origin_lng = models.DecimalField(max_digits=20, decimal_places=10)
    destination_lat = models.DecimalField(max_digits=20, decimal_places=10)
    destination_lng = models.DecimalField(max_digits=20, decimal_places=10)
    date_generation = models.DateTimeField()
