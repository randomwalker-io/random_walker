import numpy as np
import scipy.stats
import math
import matplotlib.pyplot as plt

def calcEucDist(x, y, center):
    return np.sqrt((x - center[0])**2 + (y - center[1])**2)

def coordToPixel(loc, locnw, locse, resx, resy):
    pixelx = np.ceil((loc[0].astype(float) - locnw[0])/(locse[0] - locnw[0]) * resx).tolist()
    pixely = np.ceil((loc[1].astype(float) - locnw[1])/(locse[1] - locnw[1]) * resy).tolist()
    return zip(pixelx, pixely)

def pixelToCoord(pixels, locnw, locse, resx, resy):
    pixelx, pixely = zip(*pixels)
    indx = pixelx/resx * (locse[0] - lownw[0]) + locnw[0]
    indy = pixely/resy * (locse[1] - lownw[1]) + locnw[1]
    return np.array([indx, indy])
    

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
        


plot = True
nLearningPoint = 5
layer = createIndexLayer(1280, 1280)
ind = coordToPixel(np.array([np.random.random(nLearningPoint),  np.random.random(nLearningPoint)]), [0, 0], [1, 1], 1280, 1280)
learningLayer = createLearningLayer(layer[0], layer[1], ind)
if(plot):
    plt.imshow(learningLayer)
    plt.show()

probLayer = definePriorLayer(layer[0], layer[1])
if(plot):
    plt.imshow(probLayer)
    plt.show()

## source the get water script
waterLayer = getIsWater([47.8922573,3.0057252], 5)

## Create the posterio layer
postLayer = probLayer * learningLayer
if(plot):
    plt.imshow(postLayer)
    plt.show()

## Create the final layer
finalLayer = probLayer * waterLayer * learningLayer
if(plot):
    plt.imshow(finalLayer)
    plt.colorbar()
    plt.show()

sampleLayer = finalLayer/finalLayer.sum()

im = Image.fromarray(np.array(finalLayer/finalLayer.max() * 255, dtype="uint8"))
im.save("test.png")


newIndex = np.random.choice(range(1280 * 1280), 1, p=sampleLayer.flatten().tolist())

