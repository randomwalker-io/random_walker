import numpy as np
import scipy.stats
import math
import matplotlib.pyplot as plt
from urllib2 import urlopen
from io import BytesIO
from PIL import Image
import scipy

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

layer = createLayer(1280, 640, (0, 0), (1, 1), (0.5, 0.5), 3, [(0.3, 0.2), (0.7, 0.1)])


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

createPriorLayer(layer)

def createFeasibleLayer(layer):
    url = "http://maps.googleapis.com/maps/api/staticmap?scale=1&center=" + str(layer['homeLocation'][0]) + "," + str(layer['homeLocation'][1]) + "&zoom=" + str(layer['zoom']) + "&size=" + str(layer['resx']) + "x" + str(layer['resy']) + "&sensor=false&visual_refresh=true&style=element:labels|visibility:off&style=feature:water|color:0x000000&style=feature:transit|visibility:off&style=feature:poi|visibility:off&style=feature:road|visibility:off&style=feature:administrative|visibility:off&key=AIzaSyCYfnPWhBaLjyclMa6KfFdMntt0X5ukndc"
    print url
    fd = urlopen(url)
    image_file = BytesIO(fd.read())
    im = Image.open(image_file)
    imrgb = np.asarray(im.convert("RGB"), dtype="float")
    ## This gives the sum of all the rgb values, only values which are
    ## non-zero are not water
    isWater = np.array(imrgb.sum(axis = 2) != 0, dtype="int")
    return isWater

createFeasibleLayer(layer)


def coordToInd(layer, location):
    indx = np.ceil((location[0] - layer['boundsw'][0])/(layer['boundne'][0] - layer['boundsw'][0]) * layer['resx'])
    indy = np.ceil((location[1] - layer['boundne'][1])/(layer['boundsw'][1] - layer['boundne'][1]) * layer['resy'])
    return(indx, indy)

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
        modLayer = (1 - distr.pdf(dist)) * 100
        learningLayer = learningLayer * modLayer
    return learningLayer/learningLayer.sum()

createLearningLayer(layer)


def indToCoord(layer, ind):
    coordx = float(ind[0])/layer['resx'] * (layer['boundne'][0] - layer['boundsw'][0]) + layer['boundsw'][0]
    coordy = float(ind[1])/layer['resy'] * (layer['boundne'][1] - layer['boundsw'][1]) + layer['boundsw'][1]
    return (coordx, coordy)
    
    



def createSingleLearningLayer(layer, newLocation):
    dimx = layer['resx']
    dimy = layer['resy']
    ind = createLayerIndex(dimx, dimy)
    maxDist = np.sqrt((dimx/2)**2 + (dimy/2)**2)
    distr = scipy.stats.norm(0, maxDist/10)
    dist = calcEucDist(ind[0], ind[1], coordToInd(layer, newLocation)).reshape(dimy, dimx)
    modLayer = (1 - distr.pdf(dist)) * 100
    return modLayer/modLayer.sum()

createSingleLearningLayer(layer, (0.3, 0.3))

## Test the whole module
layer = createLayer(640, 320, (0, 0), (1, 1), (0.5, 0.5), 3, [(0.3, 0.2), (0.7, 0.1)])

priorLayer = createPriorLayer(layer)
learningLayer = createLearningLayer(layer)
feasibleLayer = createFeasibleLayer(layer)
finalLayer = priorLayer * learningLayer * feasibleLayer

normalisedFinalLayer = finalLayer/finalLayer.sum()
im = Image.fromarray(np.array(normalisedFinalLayer * 255, dtype="uint8"))
im.save("test.png")

newIndex = np.random.choice(np.arange(layer['resx'] * layer['resy']) + 1, 1, p=normalisedFinalLayer.flatten())

newIndex = np.random.choice(204800 + 1, 1, p=normalisedFinalLayer.flatten())

probs = normalisedFinalLayer.flatten().tolist()
np.random.choice(len(probs), 1, probs)


## NOTE (Michael): Need to double check this!!!
def newLocationIndex(layer, finalLayer):
    probs = finalLayer.flatten().tolist()
    ind = int(np.random.choice(len(probs), 1, probs))
    indx = ind%layer['resx']
    indy = ind/layer['resy']
    return (indx, indy)

newLocInd = newLocationIndex(layer, normalisedFinalLayer)

indToCoord(layer, newLocInd)

plt.imshow(finalLayer)
plt.show()


plt.imshow(learningLayer)
plt.show()


plt.imshow(priorLayer)
plt.show()

newDestinationLayer = createSingleLearningLayer(layer, (0.5, 0.7))
finalLayerUpdated = finalLayer * newDestinationLayer

plt.imshow(finalLayerUpdated)
plt.show()

