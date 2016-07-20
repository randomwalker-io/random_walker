#!bin/bash

# This is a script to build the Random Walker Docker image
# -----------------------------------------------------------------------

# Initialisation
rootDir=$(pwd)
dockerRepo="mkao006"
appName="random_walker"

## Get the Git branch
GIT_BRANCH=$(git rev-parse --abbrev-ref HEAD)

## Get the latest Git release version
GIT_VERSION=$(git describe --abbrev=0| awk '{gsub("[a-zA-Z]", "")}1')
# list doesn't work, so we will do it manually
V_MAJOR=$(echo $GIT_VERSION | tr '.' ' ' | awk '{print $1}')
V_MINOR=$(echo $GIT_VERSION | tr '.' ' ' | awk '{print $2}')
V_PATCH=$(echo $GIT_VERSION | tr '.' ' ' | awk '{print $3}')

## Bump the version
echo "Current Git version : $GIT_VERSION"
V_PATCH=$((V_PATCH + 1))
SUGGESTED_VERSION="$V_MAJOR.$V_MINOR.$V_PATCH"

## Prompt if the version should be different
read -p "Enter a version number to build Docker [$SUGGESTED_VERSION]: "\
     dockerVersion
if [ "$dockerVersion" = "" ];
then
    dockerVersion=$SUGGESTED_VERSION
fi
echo "Will set new Docker version to be $dockerVersion"

## Build the image
sudo docker build -t $dockerRepo"/"$appName":"$dockerVersion -t $dockerRepo"/"$appName":latest" .

## remove old image
sudo docker images | \
    grep \<none\> | \
    tr -s ' '| \
    cut -d ' ' -f 3 | \
    xargs sudo docker rmi -f

## If on the master branch, then also push to the Docker hub
if [ "$GIT_BRANCH" = "master" ];
then
    sudo docker push $dockerRepo"/"$appName":"$dockerVersion
    sudo docker push $dockerRepo"/"$appName":latest"
fi

