from json import loads, dumps
import geojson as gjs
from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect, csrf_exempt, requires_csrf_token
from django_mobile import get_flavour
from django.contrib.gis.geos import Point, fromstr, Polygon
import ProbLayer as pl
from .models import Location

# Create your views here.

# @login_required
def index(request):
    """
    Returns the Random Walker web page according to device
    """

    if get_flavour() != 'full':
        return render(request, 'random_walker_engine/_m_random_walker_engine.html')
    else:
        return render(request, 'random_walker_engine/_random_walker_engine.html')

@requires_csrf_token
def newDestination(request):
    """
    Generates a new random location
    """

    if request.method == 'POST':
        # initialisation
        # -------------------------------------------------------------------------------
        username = request.user
        print username
        print "Is user anonymous: " + str(request.user.is_anonymous())
        
        # Load data and create the Grid class
        json_data = loads(request.body)
        zoom = json_data['zoom']
        center = {'lat': json_data['lat'], 'lng': json_data['lng']}
        bounds = {'southWest': {'lat': json_data['boundsw']['lat'],
                                'lng': json_data['boundsw']['lng']},
                  'northEast': {'lat': json_data['boundne']['lat'],
                                'lng': json_data['boundne']['lng']}}
        size = {'lat': json_data['size']['y'], 'lng': json_data['size']['x']}
        if not request.user.is_anonymous():
            learningPoints = getPriorDestination(username, bounds)
        print "Data loaded\n"

        # Create the grid for probability evaluation
        newGrid = pl.Grid(center, bounds, size, zoom)
        print "Grid created\n"
        
        
        # Create the layers
        # -------------------------------------------------------------------------------

        # Create the prior layer
        priorLayer = pl.createPriorLayer(newGrid, 20)
        print "Prior layer created\n"

        # Create the learning layer
        if not request.user.is_anonymous():
            learningLayer = pl.createLearningLayer(newGrid, 'normal', 0.3, learningPoints)
        print "Learning layer created\n"

        # Create the feasible layer
        feasibleLayer = pl.createFeasibleLayer(newGrid)
        print feasibleLayer.probLayer
        print "Feasible layer created\n"

        # Create the final layer
        if not request.user.is_anonymous():
            print "Computing complete final layer"
            finalLayer = priorLayer * learningLayer * feasibleLayer
        else: 
            print "Learning layer excluded in the computation"
            finalLayer = priorLayer * feasibleLayer
        print "Final layer created\n"

        # Sample the destination from the final layer
        newDestination = finalLayer.sample()
        print "New destination sampled"

        ## Save the destination
        if not request.user.is_anonymous():
            saveNewDestination(username,
                               origin=(center['lat'], center['lng']),
                               destin=newDestination)
        print "New destination saved"

        # Return the destination
        return HttpResponse(dumps(newDestination),
                            content_type="application/json")

    
def getPriorDestination(username, bounds=None):
    """
    Function to obtain user's previous locations
    """

    if not User.objects.filter(username=username).exists():
        print "User does not exist"

    # Get user object
    user = User.objects.get(username=username)

    # Check whether bounds is specified and query user previous
    # location in the bounds
    if bounds is None:
        prior_points = Location.objects.filter(user_id=user.id)

    else:
        xmin = bounds['southWest']['lat']
        xmax = bounds['northEast']['lat']
        ymin = bounds['southWest']['lng']
        ymax = bounds['northEast']['lng']
        bbox = (xmin, ymin, xmax, ymax)
        geom = Polygon.from_bbox(bbox)
        prior_points = Location.objects.filter(destin__contained=geom, user_id=user.id)
    return prior_points.values('destin')


def saveNewDestination(username, origin, destin):
    """
    Save location back to the data base
    """

    user = User.objects.get(username=username)
    user.location_set.create(
        origin = Point(origin[0], origin[1]),
        destin = Point(destin[0], destin[1]),
        date_generation = timezone.now()
    )


def show_previous_points(request):
    """ 
    Query previous points and return the geojson for plot
    """
    username = request.user
    previous_points = getPriorDestination(username)
    geojson_points = [gjs.Point((pts['destin'].get_y(), pts['destin'].get_x())) for pts in previous_points]
    previous_points_geojson = gjs.FeatureCollection([gjs.Feature(geometry=pts) for pts in geojson_points])
    return HttpResponse(json.dumps(previous_points_geojson), content_type="application/json")
