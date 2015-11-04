import numpy as np
import matplotlib.pyplot as plt
import scipy.stats

## Parameters front the JS front end
size = {'lat': 512, 'lng': 1024}
bounds = {'_southWest': {'lat': -37.13842453422676, 'lng': 174.05914306640625}, 
          '_northEast': {'lat': -36.57583533849175, 'lng': 175.46539306640625}}
center = {'lat': -36.85764758564406, 'lng': 174.76226806640625}

## Generate previous locations
nRand = 50
latRand = np.random.uniform(bounds['_northEast']['lat'], bounds['_southWest']['lat'], nRand)
lngRand = np.random.uniform(bounds['_northEast']['lng'], bounds['_southWest']['lng'], nRand)
# latRand = np.random.normal(center['lat'], 0.05, nRand)
# lngRand = np.random.normal(center['lng'], 0.15, nRand)
# latRand = center['lat']
# lngRand = center['lng']


## Construct coordinate matrix
latMat = np.linspace(bounds['_northEast']['lat'], bounds['_southWest']['lat'], size['lat']).repeat(size['lng']).reshape(size.values())
lngMat = np.linspace(bounds['_southWest']['lng'], bounds['_northEast']['lng'], size['lng']).repeat(size['lat']).reshape(size.values(), order = "F")

plt.imshow(latMat)
plt.show()


plt.imshow(lngMat)
plt.show()


## Construct Prior layer
diagDist = np.sqrt(((bounds['_northEast']['lat'] - bounds['_southWest']['lat'])/2)**2 +  
                   ((bounds['_northEast']['lng'] - bounds['_southWest']['lng'])/2)**2)
distr = scipy.stats.norm(0, diagDist)
unpl = distr.pdf(np.sqrt((latMat - center['lat'])**2 + (lngMat - center['lng'])**2))
npl = unpl/unpl.sum()

plt.imshow(npl)
plt.show()


## Construct Learning layer
positions = np.vstack([lngMat.ravel(), latMat.ravel()])
values = np.vstack([lngRand, latRand])
## NOTE (Michael): Python only supports bandwith for one direction
kernel = scipy.stats.gaussian_kde(values, bw_method=0.5)
unll = np.reshape(kernel(positions), size.values())
nll = unll/unll.sum()

ymax, ymin, xmax, xmin = bounds['_northEast']['lat'], bounds['_southWest']['lat'], bounds['_northEast']['lng'], bounds['_southWest']['lng']


fig = plt.figure()
ax = fig.add_subplot(111)
ax.imshow(nll, #cmap=plt.cm.gist_earth_r,
          extent=[xmin, xmax, ymin, ymax])
ax.plot(lngRand, latRand, 'k.', markersize=10)
ax.set_xlim([xmin, xmax])
ax.set_ylim([ymin, ymax])
plt.show()

## Contruct Feasible layer
##
## NOTE (Michael): One way of doing this is acutally use mapnik to
##                 render the map on server.
from urllib2 import urlopen
from io import BytesIO
from PIL import Image


imgUrl = "https://api.mapbox.com/v4/mapbox.streets/174.7621796,-36.857992,10/1024x512.png?access_token=pk.eyJ1IjoibWthbzAwNiIsImEiOiJjaWVyamV5MnkwMXFtOXRrdHRwdGw4cTd0In0.H28itS1jvRgLZI3JhirtZg"

fd = urlopen(imgUrl)
image_file = BytesIO(fd.read())
im = Image.open(image_file)

plt.imshow(im)
plt.show()

imar = np.asarray(im)
plt.imshow(imar)
plt.show()

imarR = 1 * (imar[:, :, 0] != 115)
imarG = 1 * (imar[:, :, 1] != 182)
imarB = 1 * (imar[:, :, 2] != 230)

## This is fine, but now we have problem with other layers such as
## border lines
unfl = imarR * imarG * imarB
plt.imshow(nfl)
plt.show()


## Construct Bias layer



## Construct sampling layer
unsl = npl * nll * unfl
nsl = unsl/unsl.sum()

plt.imshow(nsl)
plt.show()


## Sample location from the prob layer
ind = np.random.choice(nfl.size, 1, p=nfl.ravel())
newPoint = {'lat': latMat.ravel()[indLat], 'lng': lngMat.ravel()[indLng]}



## NOTE (Michael): The final layer should be passed back to the user,
##                 the in the next query it can be passed to the
##                 engine without recalculation.

