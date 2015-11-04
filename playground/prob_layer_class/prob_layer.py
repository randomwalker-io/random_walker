import numpy as np
import scipy.stats

## Define a grid class
grid = {
    lat: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    lng: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    center: [5.5, 5.5],
    bounds: [1, 1, 10, 10],
    size: [10, 10]
}

## Define a probLayer class

## Define a probPointLayer class

## Define a probPolygonLayer class

## Define a method for creating prior layer
##
## NOTE (Michael): The probability will depends on the kernel type.
def createPriorLayer(grid, kernelType, bandwidth):
    '''Method for creating the prior layer'''

## Define a method for creating learning layer
def createLearningLayer(grid, kernelType, bandwidth, learningPoints):
    '''Method for creating the learning layer'''

## Define a method for creating feasible layer
##
## NOTE (Michael): input can be either an image of the same dimension
##                 or a polygon.
def createFeasibleLayer(grid, image, polygon):
    ''' Method for creating the feasible layer'''

## Define a method for creating bias layer
##

def createBiasLayer(grid, kernelType, bandwidth, biasPoints):


