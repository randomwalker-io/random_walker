FROM ubuntu:14.04

# Set the file maintainer
MAINTAINER Michal Kao

# Set env variables used in this Dockerfile (add a unique prefix, such as DOCKYARD)
# Local directory with project source
ENV DOCKYARD_SRC=/
# Directory in container for all project files
ENV DOCKYARD_SRVHOME=/srv

# Update the default application repository sources list
RUN apt-get update && apt-get -y upgrade
RUN apt-get install -y \
    python \
    python-dev \
    python-pip \
    python-setuptools \
    software-properties-common \
    python-software-properties \
    wget

## These are required for postgis
RUN apt-get update && apt-get -y -q install \
    build-essential \
    libxml2-dev \
    libproj-dev \
    libjson0-dev \
    xsltproc \
    docbook-xsl \
    docbook-mathml \
    libgdal1-dev

## The following is necessary for python to run psycopg2 and postgresql
RUN apt-key adv --keyserver keyserver.ubuntu.com\
     --recv-keys B97B0AFCAA1A47F044F244A07FCC7D46ACCC4CF8
RUN echo "deb http://apt.postgresql.org/pub/repos/apt/ precise-pgdg main" >\
     /etc/apt/sources.list.d/pgdg.list
RUN add-apt-repository -y ppa:ubuntugis/ubuntugis-unstable
RUN apt-get update && apt-get -y -q install \
    postgresql-9.3 \
    postgresql-client-9.3 \
    postgresql-contrib-9.3\
    postgresql-server-dev-9.3\
    # postgresql-9.3-postgis-2.1 \
    libpq-dev \
    python-psycopg2

## Build Geos, requirement for PostGis
RUN wget http://download.osgeo.org/geos/geos-3.3.8.tar.bz2 \
    && tar xvfj geos-3.3.8.tar.bz2 \
    && cd geos-3.3.8 \
    && ./configure \
    && make \
    && make install \
    && cd ..

## Install PostGis
RUN wget http://download.osgeo.org/postgis/source/postgis-2.1.8.tar.gz \
    && tar xfvz postgis-2.1.8.tar.gz \
    && cd postgis-2.1.8 \
    && ./configure \
    && make \
    && make install \
    && ldconfig \
    && make comments-install \
    && cd ..

# Configure postgres
USER postgres
RUN /etc/init.d/postgresql start \
    && psql -c "CREATE USER root WITH SUPERUSER PASSWORD 'password';" \
    && createdb -O root LocationDB \
    && psql -d LocationDB -c "CREATE EXTENSION postgis";

USER root
RUN echo "host all  all    0.0.0.0/0  md5" >> /etc/postgresql/9.3/main/pg_hba.conf
RUN echo "listen_addresses='*'" >> /etc/postgresql/9.3/main/postgresql.conf

RUN mkdir -p /var/run/postgresql && chown -R postgres /var/run/postgresql
VOLUME  ["/etc/postgresql", "/var/log/postgresql", "/var/lib/postgresql"]

# Port to expose
EXPOSE 5432

# Copy entrypoint script into the image
WORKDIR $ENV DOCKYARD_SRC
COPY ./docker-entrypoint.sh /
ENTRYPOINT ["/docker-entrypoint.sh"]