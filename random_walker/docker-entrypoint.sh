#!/bin/bash

set -e

## Remove copied migrations
echo "Initialising  migration ..."
rm -r random_walker_engine/migrations/*
touch random_walker_engine/migrations/__init__.py
rm -r user_action/migrations/*
touch user_action/migrations/__init__.py

## Make migration
python manage.py makemigrations
python manage.py migrate

## Collect static files
python manage.py collectstatic --noinput

## Create log directory for uwsgi
mkdir -p /var/log/uwsgi/

## Move uwsgi configuration file to appropriate location
mkdir -p /etc/uwsgi/sites/
cp random_walker.ini /etc/uwsgi/sites/

## Start the web and application server.
echo "Starting uwsgi ..."
uwsgi --ini /etc/uwsgi/sites/random_walker.ini --gid www-data --uid www-data

