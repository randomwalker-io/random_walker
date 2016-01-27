from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect, csrf_exempt, requires_csrf_token
from django.template import RequestContext
from django.contrib.auth.models import User
from models import UserProfile
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django_mobile import get_flavour
from geojson import Feature, Point, FeatureCollection

# Create your views here.

def sign_up(request):
    if get_flavour() != 'full':
        return render(request, 'registration/_m_sign_up.html')
    else:
        return render(request, 'registration/_sign_up.html')

@requires_csrf_token
def create_user(request):
    if request.method == 'POST':
        username = request.POST.get('Username', '')
        password = request.POST.get('Password', '')
        first_name = request.POST.get('First_name', '')
        last_name = request.POST.get('Last_name', '')
        email = request.POST.get('Email', '')
        print "New user " + username + " created!"
    u = User.objects.create_user(
        username = username,
        password = password,
        email = email,
        first_name = first_name,
        last_name = last_name
    )
    u.save()
    return render(request, 'random_walker/index.html')
    # NOTE (Michael): We will create the extended profile later
    #
    # u.userprofile(
    #     address = "my home",
    #     gender = "M",
    #     date_registration = timezone.now()
    # )

def login_view(request):
    if get_flavour() != 'full':
        return render(request, 'registration/_m_login.html')
    else:
        return render(request, 'registration/_login.html')

    

def auth_view(request):
    username = request.POST.get('Username', '')
    password = request.POST.get('Password', '')
    user = authenticate(username = username, password = password)
    print user
    if user is not None:
        if user.is_active:
            login(request, user)
            print "User is logged in"
            # return HttpResponse("User is logged in!")
            return HttpResponseRedirect('/random_walker_engine/')
        else:
            print "User is inactive"
            return HttpResponseRedirect('/registration/sign_up/')
    else:
        print "User does not exist, prompt to sign in!"
        return HttpResponseRedirect('/registration/sign_up/')


def logout_view(request):
    if request.user.is_authenticated():
        logout(request)
        return HttpResponseRedirect('/')

## This is duplicated in the views.py in random_walker_engine
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


def profile_view(request, username):
    previous_points = getPriorDestination(username)    
    points_json = [Point(x) for x in zip(previous_points['lng'], previous_points['lat'])]
    feature_collection_json = FeatureCollection([Feature(geometry = x) for x in points_json])
    center = {'lat': max(previous_points['lat']) - 
              (max(previous_points['lat']) - min(previous_points['lat']))/2,
              'lng': max(previous_points['lng']) - 
              (max(previous_points['lng']) - min(previous_points['lng']))/2}
    ## Remove the hard coding of the zoom, also check why there is a home in Panama!!!
    url = 'https://api.mapbox.com/v4/mkao006.cierjexrn01naw0kmftpx3z1h/geojson(' + str(feature_collection_json) + ")/" +  str(center['lng']) + "," + str(center['lat']) + ',3/1280x512.jpg?access_token=pk.eyJ1IjoibWthbzAwNiIsImEiOiJjaWVyamV5MnkwMXFtOXRrdHRwdGw4cTd0In0.H28itS1jvRgLZI3JhirtZg'
    return render(request, 'registration/_profile.html', context={'img': url})
