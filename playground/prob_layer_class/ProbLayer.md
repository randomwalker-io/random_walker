# This is the documentation of the Random Walker layer generationg algorithm

The documentation describes a `Grid` class which has method to
generate different layers required for the Random Walker engine.


## The Grid Class

To create an object of `Grid` class, the *center*, *bounds*, *size*
are required.

The center is a dictionary with latitude and longitude corresponding
to the center of the grid.

```
{
	'lat': -36.85, 
	'lng': 174.76
}

```

The bounds specifies the bounding box of the grid. The specification
is similar to those of Leaflet.

```
{
	'southWest': {'lat': -37.13, 'lng': 174.05}, 
        'northEast': {'lat': -36.57, 'lng': 175.46}
}
```

Lastly, the size is required. It is equivalent to the number of pixel
for the grid.

```
{
	'lat': 512, 
	'lng': 1024
}
```


## Methods

### createPriorLayer

The prior layer is the layer in which determines the default search
pattern of the walker. It can be uniform, or centered at a certain
location with reduction in probability as we move further away from
the point.

To generate a prior layer grid, a single parameter *bandwidth* is
required. The bandwidth governs the serch size of the individual. The
larger the bandwidth, the greater the search area of the individual.

### createLearningLayer

A learning layer is one which modifies the probability by reducing the
probability of certain areas which has been visited previously.

To generate we need the kernelType, bandwidth and learningPoints.

kernelType corressponds to the distribution of the smoothing and the
shape of the search area, while the bandwidth is identical to the
bandwidth parameter in the prior layer.

A set of learning points is required, they need to of the following
form.

```
{
	'lat': [-36.85 , -38.89, -30.83],
	'lng': [170.77,  174.75,  184.84]
}
```

In the current implementation, the Gaussian Kernel is used to
determine the density.


### createBiasLayer

The aim of the bias layer is to bias against certain area of the
grid. The use of the layer includes biase user towards ares in the
grid where data are lacking. This will promote people to explore areas
which are lesser populated and at the same time increase the chance of
data collection.

Currently, this method is identical with the learning layer, except
learning points are replaced by biase points and has the same
data structure.