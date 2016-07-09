#!/bin/bash
echo Starting postgres
exec start-stop-daemon --start --chuid postgres:postgres \
     --exec /usr/lib/postgresql/9.3/bin/postgres -- \
     -D /var/lib/postgresql/9.3/main \
     -c config_file=/etc/postgresql/9.3/main/postgresql.conf &

python manage.py migrate                  # Apply database migrations
python manage.py collectstatic --noinput  # Collect static files

## Create log directory for uwsgi
mkdir -p /var/log/uwsgi/

## Move uwsgi configuration file to appropriate location
mkdir -p /etc/uwsgi/sites/
mv random_walker.ini /etc/uwsgi/sites/
mv uwsgi.conf /etc/init/

## Move Nginx configuration to appropriate location
mv random_walker.conf /etc/nginx/sites-available/
ln -fs /etc/nginx/sites-available/random_walker.conf /etc/nginx/sites-enabled

## Start the web and application server.
# service uwsgi start
# uwsgi --emperor /etc/uwsgi/sites --gid www-data --uid root&
uwsgi --ini /etc/uwsgi/sites/random_walker.ini --gid www-data --uid root &
service nginx start


