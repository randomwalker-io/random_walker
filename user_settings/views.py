from django.shortcuts import render, get_object_or_404
from django_mobile import get_flavour
from django.contrib.auth.models import User
from django.views.generic import DetailView
from .models import UserProfile

# Create your views here.

class UserProfileView(DetailView):
    model = UserProfile
    template_name = 'user_settings/_user_profile.html'
    context_object_name = "profile"

    def get_object(self):
        self.user = get_object_or_404(User, username=self.kwargs['username'])
        return UserProfile.objects.filter(user=self.user).get()
