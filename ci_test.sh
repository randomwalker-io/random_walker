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
