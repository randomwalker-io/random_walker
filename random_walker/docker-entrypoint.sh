#!/bin/bash

set -e

# ## Wait for postgres to start up first
# if [ "$#" -eq 0 ]
# then
#     host="localhost"
# else
#     host="$1"
#     shift
# fi

# until psql -h "$host" -U "postgres" -c '\l'; do
#     >&2 echo "Postgres is unavailable - sleeping"
#     sleep 1
# done

# >&2 echo "Postgres is up - Starting Random Walker."

## Remove copied migrations
echo "Initialising  migration ..."
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
cp random_walker.ini /etc/uwsgi/sites/

## Start the web and application server.
echo "Starting uwsgi ..."
uwsgi --ini /etc/uwsgi/sites/random_walker.ini --gid www-data --uid www-data

