#!bin/bash

# kill the deployment, the image name should probably be passed
appName="random_walker"
GIT_BRANCH=$(git rev-parse --abbrev-ref HEAD)

if [ "$GIT_BRANCH" = "dev" ]
then
    echo "The server already stopped"
elif [ "$GIT_BRANCH" = "master" ]
then
    sudo docker ps | grep $appName | awk "{print $1}" | xargs docker kill
elif [ "$GIT_BRANCH" = "production" ]
then
    echo "Production not yet implemented"
else
    echo "You are in the wrong branch for deployment"
fi

