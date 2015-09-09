import numpy as np
from urllib2 import urlopen
from io import BytesIO
from PIL import Image


def getIsWater(homeLocation, zoom):
        url = "http://maps.googleapis.com/maps/api/staticmap?scale=2&center=" + str(homeLocation[0]) + "," + str(homeLocation[1]) + "&zoom=" + str(zoom) + "&size=1024x1024&sensor=false&visual_refresh=true&style=element:labels|visibility:off&style=feature:water|color:0x000000&style=feature:transit|visibility:off&style=feature:poi|visibility:off&style=feature:road|visibility:off&style=feature:administrative|visibility:off&key=AIzaSyCYfnPWhBaLjyclMa6KfFdMntt0X5ukndc"
        fd = urlopen(url)
        image_file = BytesIO(fd.read())
        im = Image.open(image_file)
        imrgb = np.asarray(im.convert("RGB"), dtype="float")
        ## This gives the sum of all the rgb values, only values which are
        ## non-zero are not water
        isWater = np.array(imrgb.sum(axis = 2) != 0, dtype="uint8")
        return isWater


test = getIsWater([-36.857992, 174.7621796], 7)
test2 = Image.fromarray(np.array(test * 255, dtype='uint8'))
test2.save("test.png")
        
import matplotlib.pyplot as plt
from PIL import Image
import urllib2 as urllib
import io
import numpy as np

param = {
    # Set home location as Auckland if failed to to geolocate
    'homeLocation': {'lat': -36.857992, 'lng': 174.7621796},
    'dist': 100000,
    'time': float("inf"),
    'budget': float("inf"),
    'Purpose': None,
    'Distribution': 'Normal',
    'Confidence': 'Normal'
}


url = "http://maps.googleapis.com/maps/api/staticmap?scale=2&center=" + str(param["homeLocation"]['lat']) + "," + str(param["homeLocation"]['lng']) + "&zoom=7&size=1024x1024&sensor=false&visual_refresh=true&style=element:labels|visibility:off&style=feature:water|color:0x000000&style=feature:transit|visibility:off&style=feature:poi|visibility:off&style=feature:road|visibility:off&style=feature:administrative|visibility:off&key=AIzaSyCYfnPWhBaLjyclMa6KfFdMntt0X5ukndc"


fd = urllib.urlopen(url)
image_file = io.BytesIO(fd.read())
im = Image.open(image_file)
imrgb = np.asarray(im.convert("RGB"), dtype="float")

## This gives the sum of all the rgb values, only values which are
## non-zero are not water
isWater = np.array(imrgb.sum(axis = 2) == 0, dtype="int")
isWater2 = isWater * isWater * 2






plt.imshow(isWater)
plt.show()


## Steps:

## (1) Read the image
## (2) determine the sum of rgb values.
## (3) values which are non-zero indicates non-water body
## (4) Convert the 2d-array to binary indicating feasible region

## NOTE: Need to watch out for the Google Logo image.

