from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
# from .models import UserProfile

class RegistrationForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name']

class UploadProfilePicture(forms.Form):
    """Image upload form"""
    profile_picture = forms.ImageField()

# class UploadProfilePicture(ModelForm):
#     class Meta:
#         model = UserProfile
#         fields = ['profile_picture']
