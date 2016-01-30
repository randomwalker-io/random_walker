from django.shortcuts import render
from models import UserProfile
from django_mobile import get_flavour
from django.contrib.auth.models import User

# Create your views here.
def profile_view(request, username):
    """
    Profile home page
    """
    user = User.objects.get(username=username)
    context = {'username': user.username,
               'first_name': user.first_name,
               'last_name': user.last_name,
               'email': user.email
    }
    print context
    if get_flavour() != 'full':
        return render(request, 'user_settings/_m_user_profile.html',
                      context=context)
    else:
        return render(request, 'user_settings/_user_profile.html',
                      context=context)


