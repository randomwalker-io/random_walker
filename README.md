[![Stories in
Ready](https://badge.waffle.io/mkao006/random_walker.png?label=ready&title=Ready)](https://waffle.io/mkao006/random_walker)

[![travis-ci-build-status](https://travis-ci.org/randomwalker-io/random_walker.svg?branch=master)(https://travis-ci.org/randomwalker-io/random_walker)

**Random Walker** is a web application built with an aim to inspire and
make exploration easy.

We believe everyone can be an explorer. An adventure does not need to
involve lengthy planning, remote location and hefty budget; it can be
spontaneous, in a neighboring quarter and minimum cost.

From discovery a new local cafe to the most off beaten track where no
traveller explored, for novice or normad, **Random Walker** is
designed to provide surprises to travellers of any given experience
and confidence.

The engine can generate customised personalised travel itinerary, and recommend
activities in order to to maximise the travelling experience.

## Setup

On how to setup the prerequisites for running the application, please see
[setup](setup.md).


## Testing

The application can be tested with

```
sudo sh test.sh
```

and then reachable from `localhost`.

## Create Docker Image

To create the Docker image, simpy run

```
sudo sh build.sh
```

Note, if currently on the `master` branch, the image is also pushed to
Dockerhub.
