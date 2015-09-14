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

def createLayer(resx, resy, boundne, boundsw, homeLocation, zoom, 
                previousLocations):
    return {'resx': resx, # Resolution of x, of the maximum index (int)
            'resy': resy, # Resolution of y, of the maximum index (int)
            'boundne': boundne, # The coordinate of the north east bound 
            'boundsw': boundsw, # The coordinate of the south west bound 
            'homeLocation' : homeLocation, # The coordinate of the home location
            'zoom': zoom, # The zoom of the map
            'previousLocations': previousLocations # list of previous locations
    }

def createLayerIndex(resx, resy):
    indx = np.tile(np.arange(resx) + 1, resx)
    indy = np.array([val for val in np.arange(resy) + 1 for _ in np.arange(resy)])
    return np.array([indx, indy])

def calcEucDist(x, y, center):
    return np.sqrt((x - center[0])**2 + (y - center[1])**2)

def createPriorLayer(layer):
    dimx = layer['resx']
    dimy = layer['resy']
    ind = createLayerIndex(dimx, dimy)
    distLayer = calcEucDist(ind[0], ind[1], [dimx/2, dimy/2]).reshape(dimx, dimy)
    maxDist = np.sqrt((dimx/2)**2 + (dimy/2)**2)
    distr = scipy.stats.norm(maxDist/3, maxDist/3)
    unnormalisedLayer = distr.pdf(distLayer)
    normalisedLayer = unnormalisedLayer/unnormalisedLayer.sum()
    return normalisedLayer

def createFeasibleLayer(layer):
    url = "http://maps.googleapis.com/maps/api/staticmap?scale=1&center=" + str(layer['homeLocation'][0]) + "," + str(layer['homeLocation'][1]) + "&zoom=" + str(layer['zoom']) + "&size=" + str(layer['resx']) + "x" + str(layer['resy']) + "&sensor=false&visual_refresh=true&style=element:labels|visibility:off&style=feature:water|color:0x000000&style=feature:transit|visibility:off&style=feature:poi|visibility:off&style=feature:road|visibility:off&style=feature:administrative|visibility:off&key=AIzaSyCYfnPWhBaLjyclMa6KfFdMntt0X5ukndc"
    fd = urlopen(url)
    image_file = BytesIO(fd.read())
    im = Image.open(image_file)
    imrgb = np.asarray(im.convert("RGB"), dtype="float")
    ## This gives the sum of all the rgb values, only values which are
    ## non-zero are not water
    isWater = np.array(imrgb.sum(axis = 2) != 0, dtype="int")
    return isWater

def coordToInd(layer, location):
    indx = np.ceil((location[0] - layer['boundsw'][0])/(layer['boundne'][0] - layer['boundsw'][0]) * layer['resx'])
    indy = np.ceil((location[1] - layer['boundne'][1])/(layer['boundsw'][1] - layer['boundne'][1]) * layer['resy'])
    return (indx, indy)


def indToCoord(layer, ind):
    coordx = float(ind[0])/layer['resx'] * (layer['boundne'][0] - layer['boundsw'][0]) + layer['boundsw'][0]
    coordy = float(ind[1])/layer['resy'] * (layer['boundne'][1] - layer['boundsw'][1]) + layer['boundsw'][1]
    return (coordx, coordy)


def createLearningLayer(layer):
    dimx = layer['resx']
    dimy = layer['resy']
    learningLayer = np.ones(dimx * dimy).reshape(dimx, dimy)
    maxDist = np.sqrt((dimx/2)**2 + (dimy/2)**2)
    distr = scipy.stats.norm(0, maxDist/10)
    ind = createLayerIndex(dimx, dimy)
    locInd = [coordToInd(layer, i) for i in layer['previousLocations']]
    for loc in locInd:
        dist = calcEucDist(ind[0], ind[1], loc).reshape(dimx, dimy)
        modLayer = 1 - distr.pdf(dist) * 100
        learningLayer = learningLayer * modLayer
    return learningLayer/learningLayer.sum()

def createSingleLearningLayer(layer, newLocation):
    dimx = layer['resx']
    dimy = layer['resy']
    ind = createLayerIndex(dimx, dimy)
    maxDist = np.sqrt((dimx/2)**2 + (dimy/2)**2)
    distr = scipy.stats.norm(0, maxDist/10)
    dist = calcEucDist(ind[0], ind[1], coordToInd(layer, newLocation)).reshape(dimx, dimy)
    modLayer = 1 - distr.pdf(dist) * 100
    return modLayer/modLayer.sum()


## NOTE (Michael): Need to double check this!!!
def newLocationIndex(layer, finalLayer):
    ind = int(np.random.choice(range(layer['resx'] * layer['resy']), 1, p = finalLayer.flatten()))
    indx = ind%layer['resx']
    indy = ind/layer['resy']
    return (indx, indy)


########################################################################
## REAL SCRIPT
########################################################################

def index(request):
    # return render_to_response('generateNewDestination/index.html')
    return render_to_response('generateNewDestination/template/generateNewDestination/index.html')

def newDestination(request):
    if request.method == 'POST':
        homeLocation = (float(request.POST.get('lat')), float(request.POST.get('lng')))
        dist = float(request.POST.get('dist'))
        zoom = int(request.POST.get('zoom'))
        boundne = (homeLocation[0] + 1, homeLocation[1] - 1)
        boundsw = (homeLocation[0] - 1, homeLocation[1] + 1)
        previousLocations = [(homeLocation[0] + 0.5, homeLocation[1] + 0.5)]

        layer = createLayer(640, 640, boundne, boundsw, homeLocation, zoom, 
                            previousLocations)

        priorLayer = createPriorLayer(layer)

        learningLayer = createLearningLayer(layer)
        feasibleLayer = createFeasibleLayer(layer)
        finalLayer = priorLayer * learningLayer * feasibleLayer
        normalisedFinalLayer = finalLayer/finalLayer.sum()
        # with open("debug.txt", "w") as f:
        #     f.write(str(np.array(normalisedFinalLayer/normalisedFinalLayer.max() * 255, dtype="uint8")))
        #     f.write(str(layer))
        #     f.close()
        im = Image.fromarray(np.array(normalisedFinalLayer/normalisedFinalLayer.max() * 255, dtype="uint8"))
        # im = Image.fromarray(np.array(feasibleLayer/feasibleLayer.max() * 255, dtype="uint8"))
        im.save("generateNewDestination/finalImage.png")
        newLocationInd = newLocationIndex(layer, normalisedFinalLayer)
        newDestination = tmp = indToCoord(layer, newLocationInd)
        # newDestination = [homeLocation[0] + np.random.normal(dist), homeLocation[1] + np.random.normal(dist)]
        # return JsonResponse(newDestination)
        return HttpResponse(json.dumps(newDestination), content_type="application/json")





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
        
