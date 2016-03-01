from django.forms import ModelForm
from django.contrib.auth.models import User

class RegistrationForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name']
