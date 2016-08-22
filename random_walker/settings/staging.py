## This is the deployment setting for Staging which uses a different database
## than local.

from .base_extended import *

DEBUG = FALSE
ALLOWED_HOST = ["localhost", ".random-walker.com"]


## Security setttings
## ---------------------------------------------------------------------

## Use secure cookie
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

