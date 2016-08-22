#!/bin/bash

# We will deploy the docker to local here.
# -----------------------------------------------------------------------

# Initialisation
dockerRepo="mkao006"
appName="random_walker"

## Get the Git branch
if [ -z $TRAVIS_BRANCH ];
then
    GIT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
else
    GIT_BRANCH=$TRAVIS_BRANCH
fi

echo "Currently building for branch "$GIT_BRANCH

## Kill ports
sudo kill `lsof -t -i :5432`
sudo kill `lsof -t -i :80`

## Start up docker compose
if [ "$GIT_BRANCH" = "dev" ];
then
    docker-compose -f docker-compose-dev.yml stop
    docker-compose -f docker-compose-dev.yml rm -f
    docker-compose -f docker-compose-dev.yml up -d
elif [ "$GIT_BRANCH" = "master" ];
then
    docker-compose stop
    docker-compose rm -f
    docker-compose up -d
else
    echo "Incorrect branch specified"
    exit 1
fi
