#! /bin/bash

## Run unit tests on the Random Walker image
echo "Performing Unit Testing on the Rand Walker Django App ..."
cd random_walker
pip install -r requirements.txt
python manage.py test
cd ..
