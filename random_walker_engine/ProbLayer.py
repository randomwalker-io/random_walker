import numpy as np
import scipy.stats
import cStringIO
from PIL import Image
import urllib

## Define a grid class
class Grid(object):
    '''
    Define class for Grid

    The class creates a grid for evaluating probability
    
    Args:
        center: the center of the grid
        bounds: a dictionary containing the north east and south west latlng bounds.
        size: the dimension of the grid as a dictionary
        zoom: the zoom associated with the map

    Returns:
        A Grid class
    '''

    def __init__(self, center, bounds, size, zoom):
        self.center = center
        self.bounds = bounds
        self.size = size
        self.lat = np.repeat(np.linspace(bounds['northEast']['lat'], 
                                         bounds['southWest']['lat'], 
                                         size['lat']), size['lng'])
        self.lng = np.tile(np.linspace(bounds['southWest']['lng'], 
                                       bounds['northEast']['lng'], 
                                       size['lng']), size['lat'])
        self.zoom = zoom

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
        
class ProbLayer(object):
    """
    Define class ProbLayer
    
    The class allows the comparison and computation of probability
    layers.

    Args:
        grid: An object of Grid class which the probability was created upon.
        probLayer: A numpy array which contains the probability associated with the grid.
    
    Returns:
        A ProbLayer class
    """

    def __init__(self, grid, probLayer):
        if probLayer.sum() != 1:
            probLayer = probLayer/probLayer.sum()
        self.grid = grid
        self.probLayer = probLayer
        
    def sample(self):
        probs = self.probLayer.flatten().tolist()
        ind = int(np.random.choice(len(probs), 1, p=probs))
        return (self.grid.lat[ind], self.grid.lng[ind])

    def __mul__(self, other):
        if(self.grid == other.grid):
            unnormLayer = self.probLayer * other.probLayer
            normLayer = unnormLayer/unnormLayer.sum()
            return ProbLayer(self.grid, normLayer)
        else:
            raise ValueError("Inputs does not have identical grid")

    def __rmul__(self, other):
        if(self.grid == other.grid):
            unnormLayer = other.probLayer * self.probLayer
            normLayer = unnormLayer/unnormLayer.sum()
            return ProbLayer(self.grid, normLayer)
        else:
            raise ValueError("Inputs does not have identical grid")
        

def createPriorLayer(grid, bandwidth):
    '''
    Method for creating the prior layer according to the Gaussian kernel.
        
    NOTE (Michael): The probability should depends on the kernel type.

    Args:
        grid: A Grid class object
        bandwidth: The bandwidth of the Gaussian kernel
    
    Returns:
        A ProbLayer class
    '''

    distr = scipy.stats.norm(0, bandwidth)
    dist = np.sqrt((grid.lat - grid.center['lat'])**2 + 
                   (grid.lng - grid.center['lng'])**2)
    unnormalisedVec = distr.pdf(dist)
    unnormalisedLayer = unnormalisedVec.reshape(grid.size.values())
    return ProbLayer(grid, unnormalisedLayer)

def createLearningLayer(grid, kernelType, bandwidth, learningPoints):
    '''
    Method for creating the learning layer

    Args:
        grid: A Grid class object
        kernelType: (Not yet implemented)
        bandwidth: The bandwidth of the kernel
        learningPoints: Point class of set of Points from previous locations
    Returns:
        A ProbLayer class
    '''

    p = len(learningPoints)
    n = grid.size['lat'] * grid.size['lng']
    learningPointsDict = {'lat': [pts['destin'].get_x() for pts in learningPoints],
                          'lng': [pts['destin'].get_y() for pts in learningPoints]
                    }
    if p == 0:
        reversedLayer = np.repeat(1.0/n, n).reshape(grid.size.values())
    elif p == 1:
        den = scipy.stats.multivariate_normal([learningPointsDict['lng'][0], learningPointsDict['lat'][0]], np.diag([1.0/np.power(bandwidth, 2), 1.0/np.power(bandwidth, 2)]))
        pos = [list(x) for x in zip(grid.lng, grid.lat)]
        unnormalisedVec = den.pdf(pos)
        unnormalisedLayer = unnormalisedVec.reshape(grid.size.values())
        reversedLayer = unnormalisedLayer.max() - unnormalisedLayer
    elif p > 1:
        positions = np.vstack([grid.lng, grid.lat])
        values = np.vstack([learningPointsDict['lng'], learningPointsDict['lat']])
        try:
            kernel = scipy.stats.gaussian_kde(values, bw_method = bandwidth)
            unnormalisedVec = np.reshape(kernel(positions), grid.size.values())
            unnormalisedLayer = unnormalisedVec.reshape(grid.size.values())
            reversedLayer = unnormalisedLayer.max() - unnormalisedLayer
        except Exception as e:
            # The constant problem is singular matrix
            reversedLayer = np.repeat(1.0/n, n).reshape(grid.size.values())
            print str(e)
    return ProbLayer(grid, reversedLayer)


def createFeasibleLayer(grid):
    '''
    Method for creating the feasible layer
    
    NOTE (Michael): Should allow inputs to be either an image of the
    same dimension or a polygon.

    Args:
        grid: A Grid class object
    
    Returns:
        A ProbLayer class object

    '''

    url = 'https://api.mapbox.com/v4/mkao006.cierjexrn01naw0kmftpx3z1h/' +  str(grid.center['lng']) + ',' + str(grid.center['lat']) + ',' + str(grid.zoom) + '/' + str(grid.size['lng']) + 'x' + str(grid.size['lat']) + '.jpg?access_token=pk.eyJ1IjoibWthbzAwNiIsImEiOiJjaWVyamV5MnkwMXFtOXRrdHRwdGw4cTd0In0.H28itS1jvRgLZI3JhirtZg'
    print url
    file = cStringIO.StringIO(urllib.urlopen(url).read())
    img = Image.open(file)
    r = np.array(img.getdata(band=0)).reshape(grid.size['lat'], grid.size['lng'])
    g = np.array(img.getdata(band=1)).reshape(grid.size['lat'], grid.size['lng'])
    b = np.array(img.getdata(band=2)).reshape(grid.size['lat'], grid.size['lng'])
    unnormalisedLayer = (((abs(r - 115) < 30) * (abs(g - 181) < 30) * (abs(b - 229) < 50)) == False) * 1.0
    return ProbLayer(grid, unnormalisedLayer)

def createBiasLayer(grid, kernelType, bandwidth, biasPoints):
    ''' 
    Method for creating the bias layer
    
    Essentially the method is identical to the learning layer
    '''
    return createLearningLayer(grid, kernelType, bandwidth, biasPoints)
