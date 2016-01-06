from django.shortcuts import render, render_to_response
from django.http import HttpResponse
import json
import ProbLayer as pl
import numpy as np
import models
from django.utils import timezone
from models import User, Location
# Create your views here.


def index(request):
    return render_to_response('random_walker_engine/random_walker_engine.html')

def newDestination(request):
    # NOTE (Michael): Change back to POST when the database is setup
    if request.method == 'POST':
        # initialisation
        nRand = 50
        user_id = 1

        # Load data and create the Grid class
        json_data = json.loads(request.body)
        with open('debug.txt', 'w') as f:
            f.write(str(json_data))
            f.close()
        zoom = json_data['zoom']
        center = {'lat': json_data['lat'], 'lng': json_data['lng']}
        bounds = {'southWest': {'lat': json_data['boundsw']['lat'],
                                'lng': json_data['boundsw']['lng']},
                  'northEast': {'lat': json_data['boundne']['lat'],
                                'lng': json_data['boundne']['lng']}}
        size = {'lat': json_data['size']['y'], 'lng': json_data['size']['x']}
        learningPoints = filterLocation(getPriorDestination(user_id), bounds)
        # learningPoints = {'lat': [], 'lng': []}
        # with open('debug.txt', 'w') as f:
        #     f.write("learning points loaded\n")
        #     f.write(str(learningPoints))
        #     f.close()
        newGrid = pl.Grid(center, bounds, size, zoom)

        # Create the layers
        priorLayer = pl.createPriorLayer(newGrid, 20)

        learningLayer = pl.createLearningLayer(newGrid, 'normal', 0.3, learningPoints)
        feasibleLayer = pl.createFeasibleLayer(newGrid)
        with open('debug.txt', 'w') as f:
            # f.write("pass")
            f.write("prior")
            f.write(str(priorLayer.probLayer))
            f.write("\n learning")
            f.write(str(learningLayer.probLayer))
            f.write("\n feasible")
            f.write(str(feasibleLayer.probLayer))
            f.close()
        finalLayer = priorLayer * learningLayer * feasibleLayer
        newDestination = finalLayer.sample()

        saveNewDestination(user_id, origin=center, new_destination=newDestination)
        return HttpResponse(json.dumps(newDestination), content_type="application/json")


def createUser(id):
    u = User(
        user_id = id,
        user_first_name = "Michael",
        user_last_name = "Kao",
        user_email = "mkao006@gmail.com",
        user_address = "home",
        user_gender = "M",
        password_salt = "abc",
        password = "password",
        user_date_registration = timezone.now()
    )
    u.save()


def getPriorDestination(id):
    if not User.objects.filter(id=id).exists():
        createUser(id)
    user = User.objects.get(id=id)
    lat = user.location_set.values_list('destination_lat', flat=True)
    lng = user.location_set.values_list('destination_lng', flat=True)
    return {'lat': lat, 'lng': lng}

def saveNewDestination(id, origin, new_destination):
    user = User.objects.get(id=id)
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
