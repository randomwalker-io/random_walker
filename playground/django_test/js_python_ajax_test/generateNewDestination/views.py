from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, render_to_response, RequestContext
import json
import numpy as np
import scipy.stats
import math


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
        isWater = np.array(imrgb.sum(axis = 2) != 0, dtype="int")
        return isWater



def calcEucDist(x, y, center):
    return np.sqrt((x - center[0])**2 + (y - center[1])**2)

def calcPixIndex(locx, locy, locnw, locse, resx, resy):
    pixelx = np.ceil((locx.astype(float) - locnw[0])/locse[0] * resx).tolist()
    pixely = np.ceil((locy.astype(float) - locnw[1])/locse[1] * resy).tolist()
    return zip(pixelx, pixely)

def createIndexLayer(resx, resy):
    indx = np.tile(np.arange(resx) + 1, resx)
    indy = np.array([val for val in np.arange(resy) + 1 for _ in np.arange(resy)])
    return np.array([indx, indy])

def definePriorLayer(indx, indy):
    dimx = indx.max()
    dimy = indy.max()
    distLayer = calcEucDist(indx, indy, [dimx/2, dimy/2]).reshape(dimx, dimy)
    maxDist = np.sqrt((dimx/2)**2 + (dimy/2)**2)
    distr = scipy.stats.norm(maxDist/3, maxDist/3)
    unnormalisedLayer = distr.pdf(distLayer)
    normalisedLayer = unnormalisedLayer/unnormalisedLayer.sum()
    return normalisedLayer

def createLearningLayer(indx, indy, center):
    dimx = indx.max()
    dimy = indy.max()
    learningLayer = np.ones(dimx * dimy).reshape(dimx, dimy)
    maxDist = np.sqrt((dimx/2)**2 + (dimy/2)**2)
    distr = scipy.stats.norm(0, maxDist/10)
    for i in range(0, len(center)):
        dist = calcEucDist(indx, indy, center[i]).reshape(dimx, dimy)
        modLayer = 1 - distr.pdf(dist) * 100
        # print modLayer.max()
        # print modLayer.min()
        learningLayer = learningLayer * modLayer
    return learningLayer/learningLayer.sum()

def isWater(request):
    if request.method == 'POST':
        # return HttpResponse("['#000000', '#FFFFFF', '#000000', '#FFFFFF']")
        # return HttpResponse(json.dumps(np.tile(['#FFFFFF', '#000000'], 128).tolist()), content_type="application/json")
        homeLocation = [request.POST.get('lat'), request.POST.get('lng')]
        zoom = request.POST.get('zoom')
        
        ## Create index layer
        indexLayer = createIndexLayer(1280, 1280)
        waterArray = getIsWater(homeLocation, zoom)
        priorArray = definePriorLayer(indexLayer[0], indexLayer[1])

        ## Hack for generating random layer
        nLearningPoint = 25
        ind = calcPixIndex(np.random.random(nLearningPoint),  np.random.random(nLearningPoint), [0, 0], [1, 1], 1280, 1280)
        learningLayer = createLearningLayer(indexLayer[0], indexLayer[1], ind)

        finalArray = priorArray * waterArray * learningLayer

        ## Try to fina a function which allows floats
        im = Image.fromarray(np.array(finalArray/finalArray.max() * 255, dtype="uint8"))
        im.save("generateNewDestination/finalImage.png")

        # im = Image.fromarray(np.array(waterArray * 255, dtype="uint8"))
        # im.save("generateNewDestination/waterImage.png")
        # return HttpResponse(json.dumps(getIsWater(homeLocation, zoom).flatten().tolist()), content_type="application/json")
        return HttpResponse("success")
        
