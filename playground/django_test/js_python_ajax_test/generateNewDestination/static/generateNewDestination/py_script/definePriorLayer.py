import numpy as np
import scipy.stats
import math
import matplotlib.pyplot as plt

def calcEucDist(x, y, center):
    return np.sqrt((x - center[0])**2 + (y - center[1])**2)

def calcPixIndex(locx, locy, locnw, locse, resx, resy):
    pixelx = np.ceil((locx.astype(float) - locnw[0])/locse[0] * resx).tolist()
    pixely = np.ceil((locy.astype(float) - locnw[1])/locse[1] * resy).tolist()
    return zip(pixelx, pixely)

def createLayerIndex(resx, resy):
    indx = np.tile(np.arange(resx) + 1, resx)
    indy = np.array([val for val in np.arange(resy) + 1 for _ in np.arange(resy)])
    return np.array([indx, indy])

def definePriorLayer(sx, sy):
    indx = np.tile(np.arange(sx), sx)
    indy = np.array([val for val in np.arange(sy) for _ in np.arange(sy)])
    distLayer = calcEucDist(indx, indy, [sx/2, sy/2]).reshape(sx, sy)
    maxDist = np.sqrt((sx/2)**2 + (sy/2)**2)
    distr = scipy.stats.norm(sx/4, maxDist/3)
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
        


plot = True

layer = createLayerIndex(1280, 1280)
ind = calcPixIndex(np.random.random(20) * 3,  np.random.random(20) * 3, [0, 0], [3, 3], 1280, 1280)
learningLayer = createLearningLayer(layer[0], layer[1], ind)
if(plot):
    plt.imshow(learningLayer)
    plt.show()

probLayer = definePriorLayer(1280, 1280)
if(plot):
    plt.imshow(probLayer)
    plt.show()

## source the get water script
waterLayer = getIsWater([-36.857992, 174.7621796], 7)

## Create the posterio layer
postLayer = probLayer * learningLayer
if(plot):
    plt.imshow(postLayer)
    plt.show()

## Create the final layer
finalLayer = probLayer * waterLayer * learningLayer
if(plot):
    plt.imshow(finalLayer)
    plt.show()


im = Image.fromarray(np.array(finalLayer/finalLayer.max() * 255, dtype="uint8"))
im.save("test.png")
