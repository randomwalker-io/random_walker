#!bin/bash

# We will deploy the docker to local here.
# -----------------------------------------------------------------------

# Initialisation
dockerRepo="mkao006"
appName="random_walker"

## Get the Git branch
GIT_BRANCH=$(git rev-parse --abbrev-ref HEAD)

## Kill ports
kill `lsof -t -i :5432`
kill `lsof -t -i :80`

## Rebuild the random walker image
# docker build ./random_walker/ -t $dockerRepo/$appName:dev
sh build.sh

## Start up docker compose
docker-compose stop
if [ "$GIT_BRANCH" = "dev" ];
then
    docker-compose -f docker-compose-dev.yml build
    docker-compose -f docker-compose-dev.yml up
elif [ "$GIT_BRANCH" = "master" ];
then
    docker-compose build
    docker-compose up
fi
