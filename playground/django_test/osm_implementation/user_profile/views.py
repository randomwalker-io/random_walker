from django.shortcuts import render, render_to_response
from django.views.decorators.csrf import csrf_protect, csrf_exempt, requires_csrf_token
from django.template import RequestContext

# Create your views here.

def sign_up(request):
    return render_to_response('user_profile/sign_up.html', context_instance=RequestContext(request))

@requires_csrf_token
def create_user(request):
    # if request.method == 'POST':
    # return render(request, 'user_profile/sign_up_successful.html', {})
    return render_to_response('user_profile/sign_up_successful.html')
    # u = User.objects.create_user(
    #     username = username,
    #     password = password,
    #     email = "mkao006@gmail.com",
    #     first_name = "Michael",
    #     last_name = "Kao"
    # )
    # u.save()
    # NOTE (Michael): We will create the extended profile later
    #
    # u.userprofile(
    #     address = "my home",
    #     gender = "M",
    #     date_registration = timezone.now()
    # )
