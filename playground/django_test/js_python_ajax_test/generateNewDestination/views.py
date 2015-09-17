from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, render_to_response, RequestContext
import json
import numpy as np
import math
from urllib2 import urlopen
from io import BytesIO
from PIL import Image
import scipy.stats
import scipy
import matplotlib.pyplot as plt
from django.db import models
from generateNewDestination.models import Person, PreviousLocation


########################################################################
## Layer class
########################################################################


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
    indx = np.tile(np.arange(resx) + 1, resy)
    indy = np.array([val for val in np.arange(resy) + 1 for _ in np.arange(resx)])
    return np.array([indx, indy])

def calcEucDist(x, y, center):
    return np.sqrt((x - center[0])**2 + (y - center[1])**2)

def createPriorLayer(layer):
    dimx = layer['resx']
    dimy = layer['resy']
    ind = createLayerIndex(dimx, dimy)
    distLayer = calcEucDist(ind[0], ind[1], [dimx/2, dimy/2]).reshape(dimy, dimx)
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
    indx = np.ceil((location[1] - layer['boundsw'][1])/(layer['boundne'][1] - layer['boundsw'][1]) * layer['resx'])
    indy = np.ceil((location[0] - layer['boundne'][0])/(layer['boundsw'][0] - layer['boundne'][0]) * layer['resy'])
    return (indx, indy)


def indToCoord(layer, ind):
    coordx = float(ind[0])/layer['resx'] * (layer['boundne'][1] - layer['boundsw'][1]) + layer['boundsw'][1]
    coordy = float(ind[1])/layer['resy'] * (layer['boundsw'][0] - layer['boundne'][0]) + layer['boundne'][0]
    return (coordy, coordx)

def createLearningLayer(layer):
    dimx = layer['resx']
    dimy = layer['resy']
    learningLayer = np.ones(dimx * dimy).reshape(dimy, dimx)
    maxDist = np.sqrt((dimx/2)**2 + (dimy/2)**2)
    distr = scipy.stats.norm(0, maxDist/10)
    ind = createLayerIndex(dimx, dimy)
    locInd = [coordToInd(layer, i) for i in layer['previousLocations']]
    for loc in locInd:
        dist = calcEucDist(ind[0], ind[1], loc).reshape(dimy, dimx)
        modLayer = distr.pdf(dist)
        if(modLayer.max() > 0):
            modLayer2 = 1 - modLayer/modLayer.max()
        else:
            modLayer2 = 1 - modLayer
        learningLayer = learningLayer * modLayer2
    return learningLayer/learningLayer.sum()

def createSingleLearningLayer(layer, newLocation):
    dimx = layer['resx']
    dimy = layer['resy']
    ind = createLayerIndex(dimx, dimy)
    maxDist = np.sqrt((dimx/2)**2 + (dimy/2)**2)
    distr = scipy.stats.norm(0, maxDist/10)
    dist = calcEucDist(ind[0], ind[1], coordToInd(layer, newLocation)).reshape(dimy, dimx)
    modLayer = distr.pdf(dist)
    if(modLayer.max() > 0):
        modLayer2 = 1 - modLayer/modLayer.max()
    else:
        modLayer2 = 1 - modLayer
    return modLayer2/modLayer2.sum()


## NOTE (Michael): Need to double check this!!!
def sampleNewLocation(layer, finalLayer):
    probs = finalLayer.flatten().tolist()
    ind = int(np.random.choice(len(probs), 1, p=probs))
    indx = ind%layer['resx'] + 1
    indy = ind/layer['resx']
    return (indx, indy)

def getPreviousLocation(id):
    p = Person.objects.get(id=1)
    lat = p.previouslocation_set.values_list("lat", flat=True)
    lng = p.previouslocation_set.values_list("lng", flat=True)
    return zip([float(x) for x in lat], [float(x) for x in lng])

def savePreviousLocation(id, previousLocation):
    p = Person.objects.get(id=1)
    p.previouslocation_set.create(
        lat = previousLocation[0],
        lng = previousLocation[1]
    )
        
########################################################################
# Create your views here.
########################################################################



def index(request):
    # return render_to_response('generateNewDestination/index.html')
    return render_to_response('generateNewDestination/template/generateNewDestination/index.html')


def newDestination(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)
        homeLocation = (json_data['lat'], json_data['lng'])
        zoom = json_data['zoom']
        boundne = (json_data['boundne']['H'], json_data['boundne']['L'])
        boundsw = (json_data['boundsw']['H'], json_data['boundsw']['L'])

        ## Get previous locations
        previousLocations = getPreviousLocation(1)
    
        ## Create the layer meta adta
        layer = createLayer(640, 320, boundne, boundsw, homeLocation, zoom, 
                            previousLocations)
        
        ## Create the sampling layer
        priorLayer = createPriorLayer(layer)
        learningLayer = createLearningLayer(layer)
        feasibleLayer = createFeasibleLayer(layer)
        finalLayer = priorLayer * learningLayer * feasibleLayer
        normalisedFinalLayer = finalLayer/finalLayer.sum()
        
        ## Sample the new location
        newLocationInd = sampleNewLocation(layer, normalisedFinalLayer)
        newDestination = indToCoord(layer, newLocationInd)

        ## Save the location back to the database
        savePreviousLocation(1, newDestination)

        ## Create the next sampling layer for plot and check
        newSingleLayer = createSingleLearningLayer(layer, newDestination)
        newSamplingLayer = finalLayer * newSingleLayer
        plt.imshow(newSamplingLayer)
        plt.savefig("generateNewDestination/finalImage.png", format="png")

        ## Debug
        # with open("debug.txt", "w") as f:
        #     f.write(str((priorLayer.max(), priorLayer.min())) + "\n")
        #     f.write(str((learningLayer.max(), learningLayer.min())) + "\n")
        #     f.write("This is the length of prob: " + str(len(normalisedFinalLayer.flatten())) + "\n")
        #     f.write("This is the ne bound: " + str(boundne) + "\n")
        #     f.write("This is the sw bound: " + str(boundsw) + "\n")
        #     f.write("Previous Locations: " + str(previousLocations) + "\n")
        #     f.write("This is the new location index: " + str(newLocationInd) + "\n")
        #     f.write("This is the probability: " + str(normalisedFinalLayer[(newLocationInd[1], newLocationInd[0])]) + "\n")
        #     f.write("This is the new destionation coord: " + str(newDestination) + "\n")
        #     f.close()
        return HttpResponse(json.dumps(newDestination), content_type="application/json")

def resetPreviousLocations(request):
    if request.method == 'GET':
        PreviousLocation.objects.filter(person__id=1).delete()
    return HttpResponse("Previous Location Deleted")



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
        
