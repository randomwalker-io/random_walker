from django.shortcuts import render, render_to_response
from django.http import HttpResponse
import json
import ProbLayer as pl
import numpy as np
import models
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
        zoom = json_data['zoom']
        center = {'lat': json_data['lat'], 'lng': json_data['lng']}

        bounds = {'southWest': {'lat': json_data['boundsw']['lat'],
                                'lng': json_data['boundsw']['lng']},
                  'northEast': {'lat': json_data['boundne']['lat'],
                                'lng': json_data['boundne']['lng']}}
        size = {'lat': json_data['size']['y'], 'lng': json_data['size']['x']}
        # size = {'lat': 512, 'lng': 1024}
        # learningPoints = {'lat': np.random.uniform(bounds['northEast']['lat'],
        #                                            bounds['southWest']['lat'], nRand),
        #                   'lng': np.random.uniform(bounds['northEast']['lng'],
        #                                            bounds['southWest']['lng'], nRand)}
        learningPoints = getPriorDestination(user_id)
        newGrid = pl.Grid(center, bounds, size, zoom)
        
        # Create the layers
        priorLayer = pl.createPriorLayer(newGrid, 20)
        learningLayer = pl.createLearningLayer(newGrid, 'normal', 0.3, learningPoints)
        feasibleLayer = pl.createFeasibleLayer(newGrid)
        finalLayer = priorLayer * learningLayer * feasibleLayer
        newDestination = finalLayer.sample()
        saveNewDestination(user_id, origin=center, new_destination=newDestination)
        return HttpResponse(json.dumps(newDestination), content_type="application/json")


def getPriorDestination(id):
    user = User.objects.get(id=id)
    lat = user.location_set.values_list('destination_lat', flat=True)
    lng = user.location_set.values_list('destination_lng', flat=True)
    return {'lat': lat, 'lng': lng}

def saveNewDestination(id, origin, new_destination):
    user = User.objects.get(id=id)
    user.location_set.create(
        origin_lat = origin[0],
        origin_lng = origin[1],
        destination_lat = new_destination[0],
        destination_lng = new_destination[1]
    )
