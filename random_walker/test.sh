#!/bin/bash

## Start postgres if it has not started
if [ -z "$(lsof -t -i :5432)" ]
then
    sudo /etc/init.d/postgresql start
fi

## Load virtualenv
. venv/bin/activate

## Start server
python manage.py runserver --setting=settings.base
