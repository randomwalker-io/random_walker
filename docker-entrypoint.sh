#!/bin/bash

## Remove copied migrations
rm -r random_walker_engine/migrations/*
touch random_walker_engine/migrations/__init__.py
rm -r user_action/migrations/*
touch user_action/migrations/__init__.py

## Make migration
python manage.py makemigrations --setting=settings.staging
python manage.py migrate --setting=settings.staging

## Collect static files
python manage.py collectstatic --noinput --setting=settings.staging

## Create log directory for uwsgi
mkdir -p /var/log/uwsgi/

## Move uwsgi configuration file to appropriate location
mkdir -p /etc/uwsgi/sites/
mv random_walker.ini /etc/uwsgi/sites/
mv uwsgi.conf /etc/init/

## Start the web and application server.
uwsgi --ini /etc/uwsgi/sites/random_walker.ini --gid www-data --uid root

