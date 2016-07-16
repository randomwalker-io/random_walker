#!/bin/bash

echo Starting postgres
exec start-stop-daemon --start --chuid postgres:postgres \
     --exec /usr/lib/postgresql/9.3/bin/postgres -- \
     -D /var/lib/postgresql/9.3/main \
     -c config_file=/etc/postgresql/9.3/main/postgresql.conf
