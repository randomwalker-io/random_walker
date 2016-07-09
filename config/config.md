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

When `Nginx` is inactive, the web client can not reach the server, and returns
the website can not be reached error.

On the other hand, when `Nginx` is up, and uWSGI` is not, a 502 bad gateway
error will be raised, and an entry like the follow will be appended in the
error_log.

```
2016/07/04 17:04:30 [error] 8488#0: *2 connect() to unix:/home/mk/Github/random_walker/web/random_walker.sock failed (111: Connection refused) while connecting to upstream, client: 127.0.0.1, server: localhost, request: "GET / HTTP/1.1", upstream: "uwsgi://unix:/home/mk/Github/random_walker/web/random_walker.sock:", host: "localhost:8000"
```


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

The **access.log** details the requests received by `Nginx`, while the
**error.log** details any error encountered by `Nginx`.
