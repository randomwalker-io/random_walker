# This is the configuration folder for the Nginx

## Configure uWSGI

To configure the uWSGI, we need to have two files. The configuration `.ini` file
and the start up script.

The file `random_walker.ini` holds the parameter for the uWSGI.

The file `uwsgi.conf` is the Upstart script.

## Configure Nginx

We need to configure Nginx in order to handle the request.

The file `random_walker.conf` contains the current configuration for the Nginx.

## Reconfigure

To reconfigure, simply modify these files then run the bash script.

