# from django.db import models
from __future__ import unicode_literals
from django.contrib.gis.db import models
from django.contrib.auth.models import User
import ProbLayer as pl
from json import loads, dumps
from django.contrib.gis.geos import Point, fromstr, Polygon
import geojson as gjs

# Create your models here.
class Location(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    origin = models.PointField(help_text='Represented as (longitude, latitude)')
    destin = models.PointField(help_text='Represented as (longitude, latitude)')
    date_generation = models.DateTimeField()
    objects = models.GeoManager()

    # def createGrid(self, center, bounds, size, zoom):
    #     self.grid = pl.Grid(center, bounds, size, zoom)

    # def getPreviousPoints(self):
    #     lat = [x.destin_get_x() for x in self.destin]
    #     lng = [y.destin_get_y() for y in self.destin]
    #     return {'lat': lat, 'lng': lng}




def get_location_history(object, bounds=None):
    """
    Function to obtain user's previous locations
    """
    # Check whether bounds is specified and query user previous
    # location in the bounds
    if bounds is None:
        prior_points = object.values_list('destin')
    else:
        xmin = bounds['southWest']['lat']
        xmax = bounds['northEast']['lat']
        ymin = bounds['southWest']['lng']
        ymax = bounds['northEast']['lng']
        bbox = (xmin, ymin, xmax, ymax)
        geom = Polygon.from_bbox(bbox)
        prior_points = object.filter(destin__contained=geom).values_list('destin')
    return prior_points


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
        self.location = Location.objects.filter(user = self.user)
        self.grid = pl.Grid(self.center, self.bounds, self.size, self.zoom)
        self.location_history = self.get_location_history()
    
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
        prior_points = self.location.filter(destin__contained=geom).values_list('destin')
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
            return gjs.FeatureCollection([gjs.Feature(geometry=pts) for pts in geojson_points])
        else:
            return {'lat': lat, 'lng': lng}

    def create_final_layer(self):
        prior_layer = self.grid.createPriorLayer(20)
        feasible_layer = self.grid.createFeasibleLayer()
        
        if not self.user.is_anonymous():
            print "Computing complete final layer"
            learning_layer = self.grid.createLearningLayer('normal', 0.3, self.location_history)
            final_layer = prior_layer * learning_layer * feasible_layer
        else: 
            print "Learning layer excluded in the computation"
            final_layer = prior_layer * feasible_layer
        print "Final layer created\n"
        return final_layer

    def sample_destination(self):
        final_layer = self.create_final_layer()
        return final_layer.sample()




# class Test():
#     def __init__(self):
#         self.first = 1
#     def test(self):
#         return self.first + 1
#     def test2(self):
#         return self.test() + 1
        
