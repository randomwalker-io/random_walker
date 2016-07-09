#!bin/bash

# kill the deployment, the image name should probably be passed
imgName="random_walker_docker_single"

sudo docker ps | grep $imgName | awk '{print $1}' | xargs sudo docker kill

