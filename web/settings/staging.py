## This is the deployment setting for Staging which uses a different database
## than local.

from .local import *

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'LocationDB',
        'USER': 'root',
        'PASSWORD': 'password',
    }
}
