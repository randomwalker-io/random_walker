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
awsConfigDir="$rootDir/config/aws/"
uwsgiConfigDir="$rootDir/config/uwsgi/"
nginxConfigDir="$rootDir/config/nginx/"
randomwalkerDir="$rootDir/web/"
uwsgiConfigFiles=$(ls $uwsgiConfigDir)
nginxConfigFiles=$(ls $nginxConfigDir)

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
read -p "Enter a version number to build Docker [$SUGGESTED_VERSION]: " dockerVersion
if [ "$dockerVersion" = "" ]; then
    dockerVersion=$SUGGESTED_VERSION
fi
echo "Will set new Docker version to be $dockerVersion"


# Move into the random walker directory to build
cd $randomwalkerDir

# First copy the Nginx and uwsgi configuration
cp $uwsgiConfigDir/* .
cp $nginxConfigDir/* .

# Build the image
sudo docker build -t $dockerRepo"/"$appName":"$dockerVersion .
# sudo docker build -t $(echo $appName":"$dockerVersion)

# then delete the configuration files.
rm $uwsgiConfigFiles
rm $nginxConfigFiles

# Move back to root
cd $rootDir

# remove old image
sudo docker images | grep \<none\> | tr -s ' '| cut -d ' ' -f 3 | xargs sudo docker rmi -f

# kill any previous running images
sudo docker ps | grep docker-entrypoint | awk '{print $1}' | xargs --no-run-if-empty sudo docker rm -f

# Kill everything on port 8080
sudo fuser -k tcp/8080

# Run the new image
sudo docker run -d -p 8080:8000 $dockerRepo"/"$appName":"$dockerVersion




# Check the deployment instances. Should only have one instance running? Maybe
# this file should be different on different branch in order to allow for
# different instances.

# Maybe we can have the same script accross different branches, but the script
# reads the branch to determine the deployment.


# Copy the configuration file for each type of deployment

# Build each deployment

# Export the type of deployment as ENV variable

