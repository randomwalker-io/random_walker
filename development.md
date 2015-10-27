# Elements of the Web Application:

```
Home
|--- The Random Walker Engine
|--- Inspiration - A blog like sharing functionality to inspire adventure
|--- Social Platform
|--- Trip Planner
```

The application should be as light and fast as possible as travellers
generally does not have access to high speed internet.

The application should also promote the user to record locations and
information which are not currently in the Open Street Map
database. (A bias level should be provided)


## The Random Walker Engine

An engine which generates random location based on the profile of the user and preferences.

No advertisement should be promoted, the recommendation should be as
neutral as possible.

### Characteristic of Travelers

1. Distance
2. Time
3. Budget
4. Purpose
5. Distribution
6. Confidence

### Classification of Trip

1. Adventurist
   Random location are generated at any possible location for maximum exploration.
2. City Explorer
   Sampling within the city
3. Weekend Trip
   Maximum travel time of 4 hours
4. Itinery
   Random location between destinations
5. Confidence Builder
   Step by step increase the time and distance of the program.

### Algorithm

The algorithm consists of several probability layers which reflects
the preference, profile and type of travel for generating the location.

* Prior Layer - A default layer
* Learning Layer - A layer which learns from past experience of the Walker.
* Feasible Layer - Layer reflecting the feasible location
* Location Bias Layer - A layer promoting the collection of data for OSM.
* Safety Layer - A layer which reflects the safety rating of the locations.

The computation of the probability layer maybe faster using GPU
computation. That is, we plot the graph, then determin the probability
based on the color value of the pixel.

## Inspiration
A blog functionality to share location and moments of adventure.

Should also share the relative location for other Walkers to explore
and attempt to find the same location as a game with rewards.

Inspiration should be classified, we want to avoid spams and promote
only genuine exploration experience.

Inspiration from other Walker should be savable, but only relative
location should be provided to promote exploration.

Inspiration should also be location adjusted.

## Social Platform
A social platform to facilitate adventures.

Friends who have saved the same location will be notified that their
companions are also interested in visiting the place and can travel
together.

Friends can only be added with trip information. How did you met, the
location and possibly a story.

## Trip Planner