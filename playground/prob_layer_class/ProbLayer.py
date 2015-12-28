import numpy as np
import scipy.stats
import cStringIO
from PIL import Image
import urllib

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
        
        NOTE (Michael): The probability will depends on the kernel type.
        '''
        distr = scipy.stats.norm(0, bandwidth)
        dist = np.sqrt((self.lat - self.center['lat'])**2 + 
                       (self.lng - self.center['lng'])**2)
        unnormalisedLayer = distr.pdf(dist)
        normalisedLayer = unnormalisedLayer/unnormalisedLayer.sum()
        return normalisedLayer.reshape(self.size.values())

    def createLearningLayer(self, kernelType, bandwidth, learningPoints):
        '''Method for creating the learning layer
        '''
        positions = np.vstack([self.lng, self.lat])
        values = np.vstack([learningPoints['lng'], learningPoints['lat']])
        kernel = scipy.stats.gaussian_kde(values, bw_method = bandwidth)
        unnormalisedLayer = np.reshape(kernel(positions), self.size.values())
        normalisedLayer = unnormalisedLayer/unnormalisedLayer.sum()
        return normalisedLayer.reshape(self.size.values())

    ## Define a method for creating feasible layer
    ##
    ## NOTE (Michael): input can be either an image of the same dimension
    ##                 or a polygon.
    def createFeasibleLayer(self, zoom):
        ''' Method for creating the feasible layer'''
        url = 'https://api.mapbox.com/v4/mkao006.cierjexrn01naw0kmftpx3z1h/' +  str(self.center['lng']) + ',' + str(self.center['lat']) + ',' + str(zoom) + '/' + str(self.size['lng']) + 'x' + str(self.size['lat']) + '.jpg?access_token=pk.eyJ1IjoibWthbzAwNiIsImEiOiJjaWVyamV5MnkwMXFtOXRrdHRwdGw4cTd0In0.H28itS1jvRgLZI3JhirtZg'
        print url
        file = cStringIO.StringIO(urllib.urlopen(url).read())
        img = Image.open(file)
        r = np.array(img.getdata(band=0)).reshape(512, 1024)
        g = np.array(img.getdata(band=1)).reshape(512, 1024)
        b = np.array(img.getdata(band=2)).reshape(512, 1024)
        feasibleLayer = (((abs(r - 115) < 30) * (abs(g - 181) < 30) * (abs(b - 229) < 50)) == False) * 1
        # feasibleLayer = (((r == 115) * (g == 181) * (b == 229)) == False) * 1
        return feasibleLayer

    ## Define a method for creating bias layer
    ##
    def createBiasLayer(self, kernelType, bandwidth, biasPoints):
        ''' Method for creating the bias layer
        
        Essentially the method is identical to the learning layer
        '''
        positions = np.vstack([self.lng, self.lat])
        values = np.vstack([biasPoints['lng'], biasPoints['lat']])
        kernel = scipy.stats.gaussian_kde(values, bw_method = bandwidth)
        unnormalisedLayer = np.reshape(kernel(positions), self.size.values())
        normalisedLayer = unnormalisedLayer/unnormalisedLayer.sum()
        return normalisedLayer.reshape(self.size.values())


