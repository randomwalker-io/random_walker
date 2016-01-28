# from django.db import models
from django.contrib.gis.db import models
from django.contrib.auth.models import User

# Create your models here.
class Location(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    origin = models.PointField(help_text='Represented as (longitude, latitude)')
    destin = models.PointField(help_text='Represented as (longitude, latitude)')
    date_generation = models.DateTimeField()
    objects = models.GeoManager()
