from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, render_to_response, RequestContext
import json
import numpy as np

# Create your views here.

def index(request):
    # return render_to_response('generateNewDestination/index.html')
    return render_to_response('generateNewDestination/template/generateNewDestination/index.html')

def newDestination(request):
    if request.method == 'POST':
        homeLocation = [request.POST.get('lat'), request.POST.get('lng')]
        dist = request.POST.get('dist')
    newDestination = [float(homeLocation[0]) + np.random.normal(dist), float(homeLocation[1]) + np.random.normal(dist)]
    # return JsonResponse(newDestination)
    return HttpResponse(json.dumps(newDestination), content_type="application/json")
    


