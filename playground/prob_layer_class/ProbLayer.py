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
    ## NOTE (Michael): Need to define an equal method
        
class ProbLayer(object):
    def __init__(self, grid, probLayer):
        self.grid = grid
        self.probLayer = probLayer
        
    def sample(self):
        probs = self.probLayer.flatten().tolist()
        ind = int(np.random.choice(len(probs), 1, p=probs))
        return (self.grid.lat[ind], self.grid.lng[ind])

    ## NOTE (Michael): Need to test when the grids are different
    def __mul__(self, other):
        if(self.grid == other.grid):

            unnormLayer = self.probLayer * other.probLayer
            normLayer = unnormLayer/unnormLayer.sum()
            return ProbLayer(self.grid, normLayer)
        else:
            raise ValueError("Input grids are not identical")

    def __rmul__(self, other):
        if(self.grid == other.grid):
            unnormLayer = other.probLayer * self.probLayer
            normLayer = unnormLayer/unnormLayer.sum()
            return ProbLayer(self.grid, normLayer)
        else:
            raise ValueError("Input grids are not identical")
        

def createPriorLayer(grid, bandwidth):
    '''Method for creating the prior layer
        
    NOTE (Michael): The probability will depends on the kernel type.
    '''
    distr = scipy.stats.norm(0, bandwidth)
    dist = np.sqrt((grid.lat - grid.center['lat'])**2 + 
                   (grid.lng - grid.center['lng'])**2)
    unnormalisedVec = distr.pdf(dist)
    normalisedVec = unnormalisedVec/unnormalisedVec.sum()
    normalisedLayer = normalisedVec.reshape(grid.size.values())
    return ProbLayer(grid, normalisedLayer)

def createLearningLayer(grid, kernelType, bandwidth, learningPoints):
    '''Method for creating the learning layer
    '''
    positions = np.vstack([grid.lng, grid.lat])
    values = np.vstack([learningPoints['lng'], learningPoints['lat']])
    kernel = scipy.stats.gaussian_kde(values, bw_method = bandwidth)
    unnormalisedVec = np.reshape(kernel(positions), grid.size.values())
    normalisedVec = unnormalisedVec/unnormalisedVec.sum()
    normalisedLayer = normalisedVec.reshape(grid.size.values())
    return ProbLayer(grid, normalisedLayer)

## NOTE (Michael): input can be either an image of the same dimension
##                 or a polygon.
def createFeasibleLayer(grid, zoom):
    ''' Method for creating the feasible layer'''
    url = 'https://api.mapbox.com/v4/mkao006.cierjexrn01naw0kmftpx3z1h/' +  str(grid.center['lng']) + ',' + str(grid.center['lat']) + ',' + str(zoom) + '/' + str(grid.size['lng']) + 'x' + str(grid.size['lat']) + '.jpg?access_token=pk.eyJ1IjoibWthbzAwNiIsImEiOiJjaWVyamV5MnkwMXFtOXRrdHRwdGw4cTd0In0.H28itS1jvRgLZI3JhirtZg'
    print url
    file = cStringIO.StringIO(urllib.urlopen(url).read())
    img = Image.open(file)
    r = np.array(img.getdata(band=0)).reshape(512, 1024)
    g = np.array(img.getdata(band=1)).reshape(512, 1024)
    b = np.array(img.getdata(band=2)).reshape(512, 1024)
    unnormalisedFeasibleLayer = (((abs(r - 115) < 30) * (abs(g - 181) < 30) * (abs(b - 229) < 50)) == False) * 1.0
    normalisedFeasibleLayer = unnormalisedFeasibleLayer/unnormalisedFeasibleLayer.sum()
    return ProbLayer(grid, normalisedFeasibleLayer)

## Define a method for creating bias layer
##
def createBiasLayer(grid, kernelType, bandwidth, biasPoints):
    ''' Method for creating the bias layer
    
    Essentially the method is identical to the learning layer
    '''
    positions = np.vstack([grid.lng, grid.lat])
    values = np.vstack([biasPoints['lng'], biasPoints['lat']])
    kernel = scipy.stats.gaussian_kde(values, bw_method = bandwidth)
    unnormalisedVec = np.reshape(kernel(positions), grid.size.values())
    normalisedVec = unnormalisedVec/unnormalisedVec.sum()
    normalisedLayer = normalisedVec.reshape(grid.size.values())
    return ProbLayer(grid, normalisedLayer)


