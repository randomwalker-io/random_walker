import numpy as np
import scipy.stats

## Define a grid class

class Grid(object):
    def __init__(self, center, bounds, size):
        self.center = center
        self.bounds = bounds
        self.size = size
        self.lat = np.repeat(np.linspace(bounds['northEast']['lat'], 
                                         bounds['southWest']['lat'], 
                                         size['lat']), size['lng'])
        self.lng = np.tile(np.linspace(bounds['southWest']['lng'], 
                                       bounds['northEast']['lng'], 
                                       size['lng']), size['lat'])
    def createPriorLayer(self, bandwidth):
        '''Method for creating the prior layer
           NOTE (Michael): The probability will depends on the kernel type.'''
        distr = scipy.stats.norm(0, bandwidth)
        dist = np.sqrt((self.lat - self.center['lat'])**2 + 
                       (self.lng - self.center['lng'])**2)
        unnormalisedLayer = distr.pdf(dist)
        normalisedLayer = unnormalisedLayer/unnormalisedLayer.sum()
        return normalisedLayer.reshape(self.size.values())

    def createLearningLayer(self, kernelType, bandwidth, learningPoints):
        '''Method for creating the learning layer'''
        positions = np.vstack([self.lng, self.lat])
        values = np.vstack([learningPoints['lng'], learningPoints['lat']])
        kernel = scipy.stats.gaussian_kde(values, bw_method = bandwidth)
        unnormalisedLayer = np.reshape(kernel(positions), self.size.values())
        normalisedLayer = unnormalisedLayer/unnormalisedLayer.sum()
        return normalisedLayer.reshape(self.size.values())

    # ## Define a method for creating feasible layer
    # ##
    # ## NOTE (Michael): input can be either an image of the same dimension
    # ##                 or a polygon.
    # def createFeasibleLayer(self, image, polygon):
    #     ''' Method for creating the feasible layer'''

    # ## Define a method for creating bias layer
    # ##
    # def createBiasLayer(self, kernelType, bandwidth, biasPoints):


