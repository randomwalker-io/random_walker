#!/bin/bash


## Configure uWSGI
##
## make directory if does not exist then copy the configuration file over
sudo mkdir -p /etc/uwsgi/sites/
sudo cp random_walker.ini /etc/uwsgi/sites/
sudo cp uwsgi.conf /etc/init/

## Configure Nginx
##
## Copy file and then make symbolic link
sudo cp random_walker.conf /etc/nginx/sites-available/
sudo ln -fs /etc/nginx/sites-available/random_walker.conf /etc/nginx/sites-enabled


## Restart Nginx and uWSGI to reload the configuration
sudo service nginx configtest
sudo service nginx restart
sudo service uwsgi stop
sudo service uwsgi start
