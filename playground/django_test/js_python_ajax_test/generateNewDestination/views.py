from django.http import HttpResponse
from django.shortcuts import render, render_to_response, RequestContext
import numpy as np

# Create your views here.

def index(request):
    # return render_to_response('generateNewDestination/index.html')
    return render_to_response('generateNewDestination/template/generateNewDestination/index.html')
    # return HttpResponse("This is a test")

def newDestination(request):
    # return [np.random.normal(), np.random.normal()]
    return HttpResponse("The new location is at [" + str(np.random.normal()) + ", " + str(np.random.normal()) + "]")


