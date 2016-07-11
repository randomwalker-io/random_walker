#!bin/bash

# kill the deployment, the image name should probably be passed
appName="random_walker"

sudo docker ps | grep $appName | awk '{print $1}' | xargs docker kill

