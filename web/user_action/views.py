from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_protect, csrf_exempt, requires_csrf_token
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django_mobile import get_flavour
from django.views.generic import DetailView
from .forms import RegistrationForm


# Create your views here.
class profile_view(DetailView):
    """
    View Profile
    """
    model = User
    template_name = 'user_action/_user_profile.html'
    context_object_name = "profile"

    def get_object(self):
        self.user = get_object_or_404(User, username=self.kwargs['username'])
        return User.objects.filter(username=self.user).get()



def sign_up(request):
    """
    Page for sign up
    """
    form = RegistrationForm()
    if get_flavour() != 'full':
        return render(request, 'user_action/_m_sign_up.html', {'form': form})
    else:
        return render(request, 'user_action/_sign_up.html', {'form': form})

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
            return HttpResponseRedirect('/random_walker_engine/')
    return render(request, 'user_action/_sign_up.html', {'form': form})

def delete_user(request):
    """
    Delete an user
    """
    if request.method == "POST":
        user = request.user
        user_input = request.POST.get("username", '')
        if user.username == user_input:
            if user.is_authenticated():
                logout(request)
                user.delete()
                return HttpResponseRedirect("/")
        else:
            return HttpResponse("User not deleted, incorrect input")


def upload_profile_pic(request):
    """
    Upload Profile Picture
    """
    if request.method == "POST":
        form = UploadProfilePicture(request.POST, request.FILES)
        if form.is_valid():
            up = UserProfile.objects.get(user = request.user)
            up.profile_picture = form.cleaned_data['profile_picture']
            up.save()
            # handle_uploaded_file(request.FILES['file'])
            return HttpResponseRedirect("/")
        else:
            form = UploadProfilePicture()
            return HttpResponse("Upload Failed")

def login_view(request):
    """
    Page for loging
    """
    form = AuthenticationForm()
    if get_flavour() != 'full':
        return render(request, 'user_action/_m_login.html', {'form': form})
    else:
        return render(request, 'user_action/_login.html', {'form': form})



def auth_view(request):
    """
    Authenticate the user
    """
    form = AuthenticationForm(data=request.POST)
    if form.is_valid():
        user = form.get_user()
        if user is not None:
            if user.is_active:
                login(request, user)
                print "User is logged in"
                return HttpResponseRedirect('/random_walker_engine/')
            else:
                print "User is inactive"
                return HttpResponseRedirect('/user_action/sign_up/')
        else:
            print "User does not exist, prompt to sign in!"
            return HttpResponseRedirect('/user_action/sign_up/')
    else:
        return render(request, 'user_action/_login.html', {'form': form})

def logout_view(request):
    """
    Log the user out
    """

    if request.user.is_authenticated():
        logout(request)
        return HttpResponseRedirect('/')

