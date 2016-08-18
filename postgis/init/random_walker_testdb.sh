#!/bin/sh

echo "
     ************************************************************************
     Creating random_walker database ...
     ************************************************************************
     "

set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
    CREATE DATABASE random_walker;
EOSQL

psql -U postgres -d postgres -c "\l"
