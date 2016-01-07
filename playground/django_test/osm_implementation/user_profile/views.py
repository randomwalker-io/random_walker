from django.shortcuts import render, render_to_response
from django.views.decorators.csrf import csrf_protect, csrf_exempt, requires_csrf_token
from django.template import RequestContext
from django.contrib.auth.models import User

# Create your views here.

def sign_up(request):
    return render_to_response('user_profile/sign_up.html', context_instance=RequestContext(request))

@requires_csrf_token
def create_user(request):
    if request.method == 'POST':
        username = request.POST.get('Username', '')
        password = request.POST.get('Password', '')
        first_name = request.POST.get('First_name', '')
        last_name = request.POST.get('Last_name', '')
        email = request.POST.get('Email', '')
        print "New user " + username + " created! with pass word as " + password
    u = User.objects.create_user(
        username = username,
        password = password,
        email = email,
        first_name = first_name,
        last_name = last_name
    )
    u.save()
    return render_to_response("home/index.html")
    # NOTE (Michael): We will create the extended profile later
    #
    # u.userprofile(
    #     address = "my home",
    #     gender = "M",
    #     date_registration = timezone.now()
    # )
