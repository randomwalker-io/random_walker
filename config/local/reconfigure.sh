#!/bin/bash


## Configure uWSGI
##
## Make a directory if does not exist for the uwsgi configuration for the Random
## Walker application. This is the conifguration which creates the socket and
## specify the process when uWSGI is started.
##
## Then we copy the iwsgi.conf which is not really a configuration file, but an
## upstart file. This is starts uWSGI with the correct permission.
sudo mkdir -p /etc/uwsgi/sites/
sudo cp random_walker.ini /etc/uwsgi/sites/
sudo cp uwsgi.conf /etc/init/

## Configure Nginx
##
## Copy file and then make symbolic link
##
## The configuration file here specify the port and server to listen to and also
## the file system. Also includes the the uwsgi socket to point to when
## communicating with uWSGI.
sudo cp random_walker.conf /etc/nginx/sites-available/
sudo ln -fs /etc/nginx/sites-available/random_walker.conf /etc/nginx/sites-enabled


## Restart Nginx and uWSGI to reload the configuration
sudo service nginx configtest
sudo service nginx restart
sudo service uwsgi stop
sudo service uwsgi start
