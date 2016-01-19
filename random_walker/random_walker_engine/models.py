from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Location(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # origin_lat = models.DecimalField(max_digits=20, decimal_places=10)
    # origin_lng = models.DecimalField(max_digits=20, decimal_places=10)
    # destination_lat = models.DecimalField(max_digits=20, decimal_places=10)
    # destination_lng = models.DecimalField(max_digits=20, decimal_places=10)
    origin_lat = models.FloatField()
    origin_lng = models.FloatField()
    destination_lat = models.FloatField()
    destination_lng = models.FloatField()
    date_generation = models.DateTimeField()
