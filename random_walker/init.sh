## The script can only be executed as root
if [ ! `whoami` = root ];
then
    echo "Please execute this script as root!"
    exit
fi

## Create directory for credential and pull credential from S3
mkdir -p random_walker/settings/credentials/
aws s3 cp s3://random-walker-config/random_walker/settings/credentials/settings.json settings/credentials/

## Activate virtual environment and then install all currently required
## packages.
virtualenv venv/
. venv/bin/activate/
pip install -r requirements.txt

