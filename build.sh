#!bin/bash

# We will deploy the docker to local here.
# -----------------------------------------------------------------------

## NOTE (Michael): Add in arguement to just run and not build.

## NOTE (Michael): The script should depend on the Git branch and deploy in
##                 different method.

# Initialisation
rootDir=$(pwd)
dockerRepo="mkao006"
appName="random_walker"
randomwalkerDir="$rootDir/web/"

## Get the Git branch
GIT_BRANCH=$(git rev-parse --abbrev-ref HEAD)

if [ "$GIT_BRANCH" = "dev" ]
then
    cd $randomwalkerDir
    . venv/bin/activate

    ## make migration
    python manage.py makemigrations --setting=settings.base
    python manage.py migrate --setting=settings.base

    ## Collect static files
    python manage.py collectstatic --noinput --setting=settings.base

    ## Start the server
    python manage.py runserver --settings=settings.base

elif [ "$GIT_BRANCH" = "master" ]
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
    if [ "$dockerVersion" = "" ]; then
        dockerVersion=$SUGGESTED_VERSION
    fi
    echo "Will set new Docker version to be $dockerVersion"

    # Build the image
    sudo docker build -t $dockerRepo"/"$appName":"$dockerVersion .

    # remove old image
    sudo docker images | \
        grep \<none\> | \
        tr -s ' '| \
        cut -d ' ' -f 3 | \
        xargs sudo docker rmi -f

    # # kill any previous running images
    # sudo docker ps | \
    #     grep docker-entrypoint | \
    #     awk '{print $1}' | \
    #     xargs --no-run-if-empty sudo docker rm -f

    # # Kill everything on port 8080
    # sudo fuser -k tcp/8080

    # # Run the new image
    # sudo docker run -d -p 8080:8000 $dockerRepo"/"$appName":"$dockerVersion

    # Send message
    # echo "Starting staging server at local:8080/"

elif [ "$GIT_BRANCH" = "production" ]
then
    echo "Production not yet implemented"
else
    echo "You are in the wrong branch for deployment"
fi



# Check the deployment instances. Should only have one instance running? Maybe
# this file should be different on different branch in order to allow for
# different instances.

# Maybe we can have the same script accross different branches, but the script
# reads the branch to determine the deployment.


# Copy the configuration file for each type of deployment

# Build each deployment

# Export the type of deployment as ENV variable

