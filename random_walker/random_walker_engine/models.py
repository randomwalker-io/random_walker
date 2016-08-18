# from django.db import models
from __future__ import unicode_literals
import geojson as gjs
import ProbLayer as pl
from json import loads, dumps
from django.contrib.gis.db import models
from django.contrib.auth.models import User
from django.contrib.gis.geos import Point, fromstr, Polygon
from django.utils import timezone

# Create your models here.
class Location(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    origin = models.PointField(help_text='Represented as (longitude, latitude)')
    destin = models.PointField(help_text='Represented as (longitude, latitude)')
    date_generation = models.DateTimeField()
    objects = models.GeoManager()

class MapParameter(object):

    def __init__(self, request):
        json_data = loads(request.body)
        self.user = request.user
        self.zoom = json_data['zoom']
        self.center = {'lat': json_data['lat'], 'lng': json_data['lng']}
        self.bounds = {'southWest': {'lat': json_data['boundsw']['lat'],
                                     'lng': json_data['boundsw']['lng']},
                       'northEast': {'lat': json_data['boundne']['lat'],
                                     'lng': json_data['boundne']['lng']}}
        self.size = {'lat': json_data['size']['y'], 'lng': json_data['size']['x']}
        if not request.user.is_anonymous():
            self.location = Location.objects.filter(user = self.user)
        print "Data loaded\n"
        self.grid = pl.Grid(self.center, self.bounds, self.size, self.zoom)
        print "Grid created\n"

    def get_location_history(self, toJson = False):
        """
        Function to obtain user's previous locations
        """

        xmin = self.bounds['southWest']['lat']
        xmax = self.bounds['northEast']['lat']
        ymin = self.bounds['southWest']['lng']
        ymax = self.bounds['northEast']['lng']
        bbox = (xmin, ymin, xmax, ymax)
        geom = Polygon.from_bbox(bbox)
        filtered_location = self.location.filter(destin__contained=geom)
        prior_points = filtered_location.values_list('destin')
        return self.transform_location_history(prior_points, toJson = toJson)

    def transform_location_history(self, object, toJson = False):
        """
        Function to transform location history from list of points class
        to latlng dictionary.
        """

        lat = [x[0].get_x() for x in object]
        lng = [y[0].get_y() for y in object]
        if toJson:
            geojson_points = [gjs.Point(pts) for pts in zip(lng, lat)]
            return gjs.FeatureCollection([gjs.Feature(geometry=pts) 
                                          for pts in geojson_points])
        else:
            return {'lat': lat, 'lng': lng}

    def create_prior_layer(self, bandwidth=20):
        return self.grid.createPriorLayer(bandwidth=bandwidth)

    def create_feasible_layer(self):
        return self.grid.createFeasibleLayer()

    def create_learning_layer(self, kernelType='normal', bandwidth=0.3):
        location_history = self.get_location_history()
        return self.grid.createLearningLayer(kernelType=kernelType, 
                                             bandwidth=bandwidth,
                                             learningPoints = location_history)

    def create_final_layer(self):
        """
        Method for constructing the final layer from all individual layer
        """

        prior_layer = self.create_prior_layer()
        print "Prior layer created\n"
        feasible_layer = self.create_feasible_layer()
        print "Feasible layer created\n"
        if not self.user.is_anonymous():
            learning_layer = self.create_learning_layer()
            print "Learning layer created\n"
            final_layer = prior_layer * learning_layer * feasible_layer
        else: 
            final_layer = prior_layer * feasible_layer
        print "Final layer created\n"
        return final_layer

    def sample_destination(self, save_new_destination = True):
        """
        Sample a new location based on the grid constructed
        """

        final_layer = self.create_final_layer()
        sample = final_layer.sample()
        print "New destination sampled"
        if save_new_destination and not self.user.is_anonymous():
            self.location.create(
                user = self.user,
                origin = Point(self.center['lat'], self.center['lng']),
                destin = Point(sample[0], sample[1]),
                date_generation = timezone.now()
            )
            print "New destination saved"
        return sample
