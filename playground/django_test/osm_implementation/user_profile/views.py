from django.shortcuts import render, render_to_response

# Create your views here.

def sign_up(request):
    return render_to_response('user_profile/sign_up.html')
