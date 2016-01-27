from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect, csrf_exempt, requires_csrf_token
from django.template import RequestContext
from django.contrib.auth.models import User
from models import UserProfile
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django_mobile import get_flavour

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
