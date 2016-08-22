#!/bin/bash

# This is a script to build the Random Walker Docker image
# -----------------------------------------------------------------------

# Initialisation
rootDir=$(pwd)
dockerRepo="mkao006"
appName="random_walker"


## Get the Git branch
if [ -z $TRAVIS_BRANCH ];
then
    GIT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
else
    if [ $TRAVIS_BRANCH -ne "master" ] || [ $TRAVIS_BRANCH -ne "dev" ];
    then
        ## Assuming it is a release build
        GIT_BRANCH="master"
    else
        GIT_BRANCH=$TRAVIS_BRANCH
    fi
fi

## Start the build, the tag will depend on the branch
if [ "$GIT_BRANCH" = "dev" ];
then
    ## Build the development image
    sudo docker build -t $dockerRepo"/"$appName":dev" ./random_walker
elif [ "$GIT_BRANCH" = "master" ];
then
    ## If not doing Continuous integration
    if [ -z $CI ];
    then
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

        ## Build the production image
        sudo docker build -t $dockerRepo"/"$appName":"$dockerVersion ./random_walker
        sudo docker build -t $dockerRepo"/"$appName":latest" ./random_walker
    else
        sudo docker build -t $dockerRepo"/"$appName":latest" ./random_walker
    fi

    # ## Push the image to Dockerhub
    # sudo docker push $dockerRepo"/"$appName":"$dockerVersion
    # sudo docker push $dockerRepo"/"$appName":latest"
else
    echo "Incorrect branch specified"
    exit 1
fi

