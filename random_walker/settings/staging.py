## This is the deployment setting for Staging which uses a different database
## than local.

from .base_extended import *

DEBUG = False
ALLOWED_HOST = ["localhost", ".random-walker.com", "randomwalker.io"]


## Security setttings
## ---------------------------------------------------------------------

## Use secure cookie
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

## Change Email backend
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
