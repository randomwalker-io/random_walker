#!bin/bash

# We will deploy the docker to local here.
# -----------------------------------------------------------------------

## NOTE (Michael): Add in arguement to just run and not build.

# Initialisation
rootDir=$(pwd)
configDir="$rootDir/config/local_docker_single/"
randomwalkerDir="$rootDir/web/"
configFiles=$(ls $configDir)

# Move into the random walker directory to build
cd $randomwalkerDir

# First copy the Nginx and uwsgi configuration
for f in $configFiles;
do
    cp $configDir/$f .
done;

# Build the image
sudo docker build -t random_walker_docker_single .

# Then delete the configuration files.
rm $configFiles

# Move back to root
cd $rootDir

# remove old image
sudo docker images | grep \<none\> | tr -s ' '| cut -d ' ' -f 3 | xargs sudo docker rmi -f

# kill any previous running images
sudo docker ps | grep docker-entrypoint | awk '{print $1}' | xargs --no-run-if-empty sudo docker rm -f

# Kill everything on port 8080
sudo fuser -k tcp/8080

# Run the new image
sudo docker run -d -p 8080:8000 random_walker_docker_single




# Check the deployment instances. Should only have one instance running? Maybe
# this file should be different on different branch in order to allow for
# different instances.

# Maybe we can have the same script accross different branches, but the script
# reads the branch to determine the deployment.


# Copy the configuration file for each type of deployment

# Build each deployment

# Export the type of deployment as ENV variable

