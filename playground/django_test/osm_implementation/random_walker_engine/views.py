from django.shortcuts import render, render_to_response
from django.http import HttpResponse
import json

# Create your views here.


def index(request):
    return render_to_response('random_walker_engine/random_walker_engine.html')

def newDestination(request):
    return HttpResponse(json.dumps((0, 0)), content_type="application/json")

