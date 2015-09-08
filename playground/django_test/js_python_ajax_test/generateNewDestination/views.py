from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, render_to_response, RequestContext
import json
import numpy as np

## For getIsWater
from urllib2 import urlopen
from io import BytesIO
from PIL import Image
import scipy

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
    



def getIsWater(homeLocation, zoom):
        url = "http://maps.googleapis.com/maps/api/staticmap?scale=2&center=" + str(homeLocation[0]) + "," + str(homeLocation[1]) + "&zoom=" + str(zoom) + "&size=1024x1024&sensor=false&visual_refresh=true&style=element:labels|visibility:off&style=feature:water|color:0x000000&style=feature:transit|visibility:off&style=feature:poi|visibility:off&style=feature:road|visibility:off&style=feature:administrative|visibility:off&key=AIzaSyCYfnPWhBaLjyclMa6KfFdMntt0X5ukndc"
        fd = urlopen(url)
        image_file = BytesIO(fd.read())
        im = Image.open(image_file)
        imrgb = np.asarray(im.convert("RGB"), dtype="float")
        ## This gives the sum of all the rgb values, only values which are
        ## non-zero are not water
        isWater = np.array(imrgb.sum(axis = 2) == 0, dtype="int")
        return isWater

def isWater(request):
    if request.method == 'POST':
        # return HttpResponse("['#000000', '#FFFFFF', '#000000', '#FFFFFF']")
        # return HttpResponse(json.dumps(np.tile(['#FFFFFF', '#000000'], 128).tolist()), content_type="application/json")
        homeLocation = [request.POST.get('lat'), request.POST.get('lng')]
        zoom = request.POST.get('zoom')
        waterArray = getIsWater(homeLocation, zoom)
        im = Image.fromarray(np.array(waterArray * 255, dtype="uint8"))
        im.save("generateNewDestination/waterImage.png")
        # return HttpResponse(json.dumps(getIsWater(homeLocation, zoom).flatten().tolist()), content_type="application/json")
        return HttpResponse("success")
        
