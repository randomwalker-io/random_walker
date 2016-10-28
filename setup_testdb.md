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

Then run the following to create the test user and database.

```
CREATE USER random_walker_tester WITH PASSWORD 'password';
ALTER USER random_walker_tester CREATEDB;
CREATE DATABASE random_walker_testdb OWNER random_walker_tester;
```

After the test user and database has been created, then you can quit
the program.
