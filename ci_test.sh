#! /bin/bash

## Run unit tests on the Random Walker image
echo "Performing Unit Testing on the Rand Walker Django App ..."
cd random_walker
pip install -r requirements.txt
python manage.py test
cd ..

## Check status
##
## NOTE (Michael): Might want to elaborate this section to test all pages.
echo "Testing home page accessibility ... "
code=$(curl -s -o /dev/null -w "%{http_code}" localhost:80)
echo $code

if [ $code = 200 ];
then
    echo "Server launched successfully"
    exit 0
else
    echo "Server launch failed"
    exit 1
fi
