from django.db import models

# Create your models here.

class Person(models.Model):
    name = models.CharField(max_length=200)
    create_time = models.DateTimeField('creation time')
    def __str__(self):
        return self.name

class PreviousLocation(models.Model):
    person = models.ForeignKey(Person)
    lat = models.DecimalField(max_digits=20, decimal_places=10)
    lng = models.DecimalField(max_digits=20, decimal_places=10)
    def __str__(self):
        return "person: " + str(self.person) + "\n" + "previousLocation: (" + str(self.lat) + "," + str(self.lng) + ")"

