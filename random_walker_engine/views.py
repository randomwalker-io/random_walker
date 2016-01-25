from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from models import Location
import json
import ProbLayer as pl
from django.views.decorators.csrf import csrf_protect, csrf_exempt, requires_csrf_token
from django_mobile import get_flavour

# Create your views here.

# @login_required
def index(request):
    if get_flavour() != 'full':
        return render(request, 'random_walker_engine/m_random_walker_engine.html')
    else:
        return render(request, 'random_walker_engine/random_walker_engine.html')

@requires_csrf_token
def newDestination(request):
    # NOTE (Michael): Change back to POST when the database is setup
    if request.method == 'POST':
        # initialisation
        username = request.user
        print username
        print "Is user anonymous: " + str(request.user.is_anonymous())
        
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
        if not request.user.is_anonymous():
            learningPoints = filterLocation(getPriorDestination(username), bounds)
        newGrid = pl.Grid(center, bounds, size, zoom)
        print newGrid
        print "Grid created\n"
        
        
        # Create the layers
        priorLayer = pl.createPriorLayer(newGrid, 20)
        print priorLayer.probLayer
        print "Prior layer created\n"
        if not request.user.is_anonymous():
            learningLayer = pl.createLearningLayer(newGrid, 'normal', 0.3, learningPoints)
            print learningLayer.probLayer
        print "Learning layer created\n"
        feasibleLayer = pl.createFeasibleLayer(newGrid)
        print feasibleLayer.probLayer
        print "Feasible layer created\n"
        if not request.user.is_anonymous():
            print "Computing complete final layer"
            finalLayer = priorLayer * learningLayer * feasibleLayer
        else: 
            print "Learning layer excluded in the computation"
            finalLayer = priorLayer * feasibleLayer

        print "Final layer created\n"
        newDestination = finalLayer.sample()
        print newDestination
        print "New destination sampled"
        if not request.user.is_anonymous():
            saveNewDestination(username, origin=center, new_destination=newDestination)
        print "New destination saved"
        return HttpResponse(json.dumps(newDestination), content_type="application/json")

    
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
    bounded_location = [(x, y) for x,y in locations \
                        if (x > bounds['southWest']['lat'] and \
                            x < bounds['northEast']['lat'] and \
                            y > bounds['southWest']['lng'] and \
                            y > bounds['southWest']['lng'])]
    bounded_location_lat = [x[0] for x in bounded_location]
    bounded_location_lng = [x[1] for x in bounded_location]
    return {'lat': bounded_location_lat, 'lng': bounded_location_lng}
