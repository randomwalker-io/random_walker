from django.shortcuts import render, render_to_response

# Create your views here.
from django.http import HttpResponse

def engine_home(request):
    return render_to_response('random_walker_engine/random_walker_engine.html')
