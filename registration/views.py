from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect, csrf_exempt, requires_csrf_token
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django_mobile import get_flavour
from geojson import Feature, Point, FeatureCollection
from .forms import RegistrationForm

# Create your views here.
def sign_up(request):
    """
    Page for sign up
    """
    form = RegistrationForm()
    if get_flavour() != 'full':
        return render(request, 'registration/_m_sign_up.html', {'form': form})
    else:
        return render(request, 'registration/_sign_up.html', {'form': form})

@requires_csrf_token
def create_user(request):
    """ 
    Create a new user
    """

    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            info = form.cleaned_data
            new_user = User.objects.create_user(**info)
            auth_user = authenticate(username = info['username'], password = info['password'])
            login(request, auth_user)
            # redirect, or however you want to get to the main view
            return HttpResponseRedirect('/random_walker_engine/')
    return render(request, 'registration/_sign_up.html', {'form': form})

def login_view(request):
    """
    Page for loging
    """
    if get_flavour() != 'full':
        return render(request, 'registration/_m_login.html')
    else:
        return render(request, 'registration/_login.html')

    

def auth_view(request):
    """
    Authenticate the user
    """

    username = request.POST.get('Username', '')
    password = request.POST.get('Password', '')
    user = authenticate(username = username, password = password)
    print user
    if user is not None:
        if user.is_active:
            login(request, user)
            print "User is logged in"
            return HttpResponseRedirect('/random_walker_engine/')
        else:
            print "User is inactive"
            return HttpResponseRedirect('/registration/sign_up/')
    else:
        print "User does not exist, prompt to sign in!"
        return HttpResponseRedirect('/registration/sign_up/')


def logout_view(request):
    """
    Log the user out
    """

    if request.user.is_authenticated():
        logout(request)
        return HttpResponseRedirect('/')
