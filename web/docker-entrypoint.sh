#!/bin/bash
python manage.py migrate                  # Apply database migrations
python manage.py collectstatic --noinput  # Collect static files

## Start uwsgi
exec uwsgi --http :8000 \
     --home /home/mk/Github/random_walker/web/venv \
     --chdir /home/mk/Github/random_walker/web/ \
     -w random_walker.wsgi
