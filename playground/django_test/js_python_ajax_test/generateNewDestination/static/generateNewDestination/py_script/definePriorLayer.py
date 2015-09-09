import numpy as np
import scipy.stats
import math

def calcEucDist(x, y, center):
    return np.sqrt((x - center[0])**2 + (y - center[1])**2)


def definePriorLayer(sx, sy):
    indx = np.tile(np.arange(sx), sx)
    indy = np.array([val for val in np.arange(sy) for _ in np.arange(sy)])
    distLayer = calcEucDist(indx, indy, [sx/2, sy/2]).reshape(sx, sy)
    maxDist = np.sqrt((sx/2)**2 + (sy/2)**2)
    dist = scipy.stats.norm(sx/4, maxDist/3)
    unnormalisedLayer = dist.pdf(distLayer)
    normalisedLayer = unnormalisedLayer/unnormalisedLayer.sum()
    return normalisedLayer


    



probLayer = definePriorLayer(1280, 1280)
plt.imshow(probLayer)
plt.show()

## source the get water script
waterLayer = getIsWater([-36.857992, 174.7621796], 7)
finalLayer = probLayer * waterLayer

import matplotlib.pyplot as plt
plt.imshow(finalLayer)
plt.show()

finalLayer/finalLayer.max() * 255
