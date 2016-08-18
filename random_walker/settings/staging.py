## This is the deployment setting for Staging which uses a different database
## than local.

from .base_extended import *

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': get_secret("RDS_DB_NAME"),
        'USER': get_secret("RDS_DB_USERNAME"),
        'PASSWORD': get_secret("RDS_DB_PASSWORD"),
        'HOST': "postgis",
        "PORT": 5432,
    }
}
