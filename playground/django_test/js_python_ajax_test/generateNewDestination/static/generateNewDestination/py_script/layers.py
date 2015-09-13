def createLayer(resx, resy, boundnw, boundse, homeLocation, zoom, 
                previousLocations):
    return {'resx': resx, # Resolution of x, of the maximum index (int)
            'resy': resy, # Resolution of y, of the maximum index (int)
            'boundnw': boundnw, # The coordinate of the north west bound 
            'boundse': boundse, # The coordinate of the south east bound 
            'homeLocation' : homeLocation, # The coordinate of the home location
            'zoom': zoom, # The zoom of the map
            'previousLocations': previousLocations # list of previous locations
    }

layer = createLayer(640, 640, (0, 0), (1, 1), (0.5, 0.5), 3, [(0.3, 0.2), (0.7, 0.1)])


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

createPriorLayer(layer)

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

createFeasibleLayer(layer)


def coordToInd(layer, location):
    indx = np.ceil((location[0] - layer['boundnw'][0])/(layer['boundse'][0] - layer['boundnw'][0]) * layer['resx'])
    indy = np.ceil((location[1] - layer['boundnw'][1])/(layer['boundse'][1] - layer['boundnw'][1]) * layer['resy'])
    return(indx, indy)

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

createLearningLayer(layer)




def createSingleLearningLayer(layer, newLocation):
    dimx = layer['resx']
    dimy = layer['resy']
    ind = createLayerIndex(dimx, dimy)
    maxDist = np.sqrt((dimx/2)**2 + (dimy/2)**2)
    distr = scipy.stats.norm(0, maxDist/10)
    dist = calcEucDist(ind[0], ind[1], coordToInd(layer, newLocation)).reshape(dimx, dimy)
    modLayer = 1 - distr.pdf(dist) * 100
    return modLayer/modLayer.sum()

createSingleLearningLayer(layer, (0.3, 0.3))

## Test the whole module
layer = createLayer(640, 640, (0, 0), (1, 1), (0.5, 0.5), 3, [(0.3, 0.2), (0.7, 0.1)])

priorLayer = createPriorLayer(layer)
learningLayer = createLearningLayer(layer)
feasibleLayer = createFeasibleLayer(layer)
finalLayer = priorLayer * learningLayer * feasibleLayer


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

