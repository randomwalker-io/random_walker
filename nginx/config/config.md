# This is the configuration folder for the Nginx

[Nginx](https://nginx.org/en/) is an HTTP and reverse proxy server, and a
generic TCP/UDP proxy server.

In order to dvelop a web application, we need two components. First of all, a
internet facing web server which handles request from external clients.
Secondly, an application server which communicates between the web server and
the application.

In this configuration, `Nginx` is used as the reverse proxy to handle external
request and process the request according to the type of the request. For
example, static files will be directly served (although not currently
implemented.), while request to generate new location will be forward to the
application.

`WSGI` is a **specification** for the communnication between the web server and
the application server. The `uWSGI` is the **application server** that handles
the communication while `uwsgi` is the **binary protocol** implemented by uWSGI
to communicate with the web server.

## Configure uWSGI

To configure the uWSGI, we need to have two files. The configuration `.ini` file
and the start up script.

The file `random_walker.ini` holds the parameter for the uWSGI.

The file `uwsgi.conf` is the Upstart script.

## Configure Nginx

We need to configure Nginx in order to handle the request.

The file `random_walker.conf` contains the current configuration for the Nginx.

## Reconfigure

To reconfigure, simply modify these files then run the *reconfigure.sh* bash
script.

## Logs

The logs of the Nginx are stored at `/var/log/nginx/`.
