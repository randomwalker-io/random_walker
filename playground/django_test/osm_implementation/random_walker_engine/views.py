from django.shortcuts import render, render_to_response
from django.http import HttpResponse
import json
import ProbLayer as pl
import numpy as np
import models
from django.utils import timezone
from django.contrib.auth.models import User
from models import UserProfile, Location
# Create your views here.


def index(request):
    return render_to_response('random_walker_engine/random_walker_engine.html')

def newDestination(request):
    # NOTE (Michael): Change back to POST when the database is setup
    if request.method == 'POST':
        # initialisation
        nRand = 50
        username = 'mkao006'

        # Load data and create the Grid class
        json_data = json.loads(request.body)
        print "Data loaded\n"
        zoom = json_data['zoom']
        center = {'lat': json_data['lat'], 'lng': json_data['lng']}
        bounds = {'southWest': {'lat': json_data['boundsw']['lat'],
                                'lng': json_data['boundsw']['lng']},
                  'northEast': {'lat': json_data['boundne']['lat'],
                                'lng': json_data['boundne']['lng']}}
        size = {'lat': json_data['size']['y'], 'lng': json_data['size']['x']}
        learningPoints = filterLocation(getPriorDestination(username), bounds)
        newGrid = pl.Grid(center, bounds, size, zoom)
        print "Grid created\n"
        
        # Create the layers
        priorLayer = pl.createPriorLayer(newGrid, 20)
        print "Prior layer created\n"
        learningLayer = pl.createLearningLayer(newGrid, 'normal', 0.3, learningPoints)
        print "Learning layer created\n"
        feasibleLayer = pl.createFeasibleLayer(newGrid)
        print "Feasible layer created\n"
        finalLayer = priorLayer * learningLayer * feasibleLayer
        print "Final layer created\n"
        newDestination = finalLayer.sample()
        print "New destination sampled"

        saveNewDestination(username, origin=center, new_destination=newDestination)
        print "New destination saved"
        return HttpResponse(json.dumps(newDestination), content_type="application/json")


# def createUser(id):
#     u = User(
#         user_id = id,
#         user_first_name = "Michael",
#         user_last_name = "Kao",
#         user_email = "mkao006@gmail.com",
#         user_address = "home",
#         user_gender = "M",
#         password_salt = "abc",
#         password = "password",
#         user_date_registration = timezone.now()
#     )
#     u.save()


def createUser(username, password):
    u = User.objects.create_user(
        username = username,
        password = password,
        email = "mkao006@gmail.com",
        first_name = "Michael",
        last_name = "Kao"
    )
    u.save()
    # NOTE (Michael): We will create the extended profile later
    #
    # u.userprofile(
    #     address = "my home",
    #     gender = "M",
    #     date_registration = timezone.now()
    # )
    
def getPriorDestination(username):
    if not User.objects.filter(username=username).exists():
        # NOTE (Michael): Here we assume the user is already
        #                 created. Otherwise, we should redirect them
        #                 to the sign-up page
        #
        # createUser(username)
        print "User does not exist"
    user = User.objects.get(username=username)
    lat = user.location_set.values_list('destination_lat', flat=True)
    lng = user.location_set.values_list('destination_lng', flat=True)
    return {'lat': lat, 'lng': lng}

def saveNewDestination(username, origin, new_destination):
    user = User.objects.get(username=username)
    user.location_set.create(
        origin_lat = origin['lat'],
        origin_lng = origin['lng'],
        destination_lat = new_destination[0],
        destination_lng = new_destination[1],
        date_generation = timezone.now()
    )

def filterLocation(location, bounds):
    locations = zip(location['lat'], location['lng'])
    bounded_location = [(x, y) for x,y in locations if (x > bounds['southWest']['lat'] and x < bounds['northEast']['lat'] and y > bounds['southWest']['lng'] and y > bounds['southWest']['lng'])]
    bounded_location_lat = [x[0] for x in bounded_location]
    bounded_location_lng = [x[1] for x in bounded_location]
    return {'lat': bounded_location_lat, 'lng': bounded_location_lng}
