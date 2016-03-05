import numpy as np
import scipy.stats
import cStringIO
from PIL import Image
import urllib
from geojson import Point, Feature, FeatureCollection

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

    def createPriorLayer(self, bandwidth):
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
        dist = np.sqrt((self.lat - self.center['lat'])**2 +
                       (self.lng - self.center['lng'])**2)
        unnormalisedVec = distr.pdf(dist)
        unnormalisedLayer = unnormalisedVec.reshape(self.size.values())
        return ProbLayer(self, unnormalisedLayer)

    def createLearningLayer(self, kernelType, bandwidth, learningPoints):
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
        n = self.size['lat'] * self.size['lng']
        if p == 0:
            reversedLayer = np.repeat(1.0/n, n).reshape(self.size.values())
        elif p == 1:
            den = scipy.stats.multivariate_normal([learningPoints['lng'][0],
                                                   learningPoints['lat'][0]],
                                                  np.diag([1.0/np.power(bandwidth, 2),
                                                           1.0/np.power(bandwidth, 2)]))
            pos = [list(x) for x in zip(self.lng, self.lat)]
            unnormalisedVec = den.pdf(pos)
            unnormalisedLayer = unnormalisedVec.reshape(self.size.values())
            reversedLayer = unnormalisedLayer.max() - unnormalisedLayer
        elif p > 1:
            positions = np.vstack([self.lng, self.lat])
            values = np.vstack([learningPoints['lng'], learningPoints['lat']])
        try:
            kernel = scipy.stats.gaussian_kde(values, bw_method = bandwidth)
            unnormalisedVec = np.reshape(kernel(positions), self.size.values())
            unnormalisedLayer = unnormalisedVec.reshape(self.size.values())
            reversedLayer = unnormalisedLayer.max() - unnormalisedLayer
        except Exception as e:
            # The constant problem is singular matrix
            reversedLayer = np.repeat(1.0/n, n).reshape(self.size.values())
            print str(e)
        return ProbLayer(self, reversedLayer)


    def createFeasibleLayer(self):
        '''
        Method for creating the feasible layer

        NOTE (Michael): Should allow inputs to be either an image of the
        same dimension or a polygon.

        Args:
        grid: A Grid class object

        Returns:
        A ProbLayer class object

        '''

        url = 'https://api.mapbox.com/v4/mkao006.cierjexrn01naw0kmftpx3z1h/' +  str(self.center['lng']) + ',' + str(self.center['lat']) + ',' + str(self.zoom) + '/' + str(self.size['lng']) + 'x' + str(self.size['lat']) + '.jpg?access_token=pk.eyJ1IjoibWthbzAwNiIsImEiOiJjaWVyamV5MnkwMXFtOXRrdHRwdGw4cTd0In0.H28itS1jvRgLZI3JhirtZg'
        print url
        file = cStringIO.StringIO(urllib.urlopen(url).read())
        img = Image.open(file)
        r = np.array(img.getdata(band=0)).reshape(self.size['lat'], self.size['lng'])
        g = np.array(img.getdata(band=1)).reshape(self.size['lat'], self.size['lng'])
        b = np.array(img.getdata(band=2)).reshape(self.size['lat'], self.size['lng'])
        unnormalisedLayer = (((abs(r - 115) < 30) * (abs(g - 181) < 30) * (abs(b - 229) < 50)) == False) * 1.0
        return ProbLayer(self, unnormalisedLayer)

    def createBiasLayer(self, kernelType, bandwidth, biasPoints):
        '''
        Method for creating the bias layer

        Essentially the method is identical to the learning layer
        '''
        return createLearningLayer(self, kernelType, bandwidth, biasPoints)

        
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

    def toGeoJsonPointFeatureCollection(self):
        prob_vec = self.probLayer.flatten()
        grid = [Point(x) for x in zip(self.grid.lat, self.grid.lng)]
        geojson = FeatureCollection([Feature(geometry=x[0], properties={'prob': x[1]}) for x  in zip(grid, prob_vec)])
        return geojson

        
