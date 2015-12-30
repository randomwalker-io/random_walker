from django.shortcuts import render, render_to_response
from django.http import HttpResponse
import json
import ProbLayer as pl
import numpy as np
# Create your views here.


def index(request):
    return render_to_response('random_walker_engine/random_walker_engine.html')

def newDestination(request):
    # NOTE (Michael): Change back to POST when the database is setup
    if request.method == 'POST':
        json_data = json.loads(request.body)

        nRand = 50
        zoom = json_data['zoom']
        center = {'lat': json_data['lat'], 'lng': json_data['lng']}

        bounds = {'southWest': {'lat': json_data['boundsw']['lat'],
                                'lng': json_data['boundsw']['lng']},
                  'northEast': {'lat': json_data['boundne']['lat'],
                                'lng': json_data['boundne']['lng']}}
        size = {'lat': json_data['size']['y'], 'lng': json_data['size']['x']}
        # size = {'lat': 512, 'lng': 1024}
        learningPoints = {'lat': np.random.uniform(bounds['northEast']['lat'],
                                                   bounds['southWest']['lat'], nRand),
                          'lng': np.random.uniform(bounds['northEast']['lng'],
                                                   bounds['southWest']['lng'], nRand)}
        ## Create new grid
        newGrid = pl.Grid(center, bounds, size, zoom)
        priorLayer = pl.createPriorLayer(newGrid, 20)
        learningLayer = pl.createLearningLayer(newGrid, 'normal', 0.3, learningPoints)
        feasibleLayer = pl.createFeasibleLayer(newGrid)
        finalLayer = priorLayer * learningLayer * feasibleLayer
        return HttpResponse(json.dumps(finalLayer.sample()), content_type="application/json")

