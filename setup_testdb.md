# Setup Test Database for Random Walker

This guide sets up a test database for local development of Random
Walker.

## Install postgres

Follow the [Installation
section](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-16-04#installation)
to install postgresql.

Then create the test user, when prompted with the password enter
`password`.

```
sudo -i -u postgres
psql
```

Then run the following to create the test user and database. We need
to make the test user as superuser in order to create the `PostGIS`
extension.

```
CREATE USER random_walker_tester WITH PASSWORD 'password';
ALTER USER random_walker_tester WITH SUPERUSER;
CREATE DATABASE random_walker_testdb OWNER random_walker_tester;
```

After the test user and database has been created, then you can quit
the program.

We also need `PostGIS` in order for Random Walker to work.

```
sudo apt-get install -y postgis postgresql-9.5-postgis-2.2
psql -U random_walker_tester -d random_walker_testdb -h localhost -c "CREATE EXTENSION postgis; CREATE EXTENSION postgis_topology;"
```
