from json import loads, dumps
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import requires_csrf_token, ensure_csrf_cookie
from django_mobile import get_flavour
from .models import Location, MapParameter

# Create your views here.

@ensure_csrf_cookie
def index(request):
    """
    Returns the Random Walker web page according to device
    """

    if get_flavour() != 'full':
        return render(request, 'random_walker_engine/_m_random_walker_engine.html')
    else:
        return render(request, 'random_walker_engine/_random_walker_engine.html')

@requires_csrf_token
def generate_new_destination(request):
    """
    Generates a new random location
    """

    if request.method == 'POST':
        params = MapParameter(request)
        request_data = loads(request.body)
        new_destination = params.sample_destination(request_data['n_sample'])

        # Return the destination
        return HttpResponse(dumps(new_destination),
                            content_type="application/json")

@requires_csrf_token
@login_required
def show_location_history(request):
    """
    Query previous points and return the geojson for plot
    """
    if request.method == 'POST':
        params = MapParameter(request)
        previous_points = params.get_location_history(toJson = True)
        return HttpResponse(dumps(previous_points),
                            content_type="application/json")
