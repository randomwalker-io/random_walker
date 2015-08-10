########################################################################
## TItle: Use Bayesian Search Theory to find best destination
## Date: 2015-08-05
########################################################################

library(ggplot2)


## Initialisation
gridSize = 30
td = 300
ed = 5

## Set up original traveller distance distribution
d = data.frame(x = rep(seq(-gridSize, gridSize), each = 61),
    y = rep(seq(-gridSize, gridSize), times = 61))
## d$PrP = dnorm(d$x, 0, sqrt(td)) * dnorm(d$y, 0, sqrt(td))
d$PrP = 1/NROW(d)

ggplot(d, aes(x = x, y = y, z = PrP)) +
    geom_point(aes(alpha = PrP)) +
        stat_contour()

## Create the distance from search point
euclideanDistance = function(x, y, x0, y0){
    dx = (x - x0)^2
    dy = (y - y0)^2
    sqrt(dx + dy)
}

## Create the search distribution
searchDistribution = function(distance){
    1 - dnorm(distance/3, sd = 1)
}

## Update distribution assuming first destination is (20, 5)
d$searchedDist = with(d, searchDistribution(euclideanDistance(x, y, 20, 5)))

ggplot(d, aes(x = x, y = y, z = searchedDist)) +
    geom_point(aes(alpha = searchedDist)) +
        stat_contour() +
            geom_point(aes(x = 20, y = 5, color = "red"))

d$uPrP = d$PrP * d$searchedDist

ggplot(d, aes(x = x, y = y, z = uPrP)) +
    geom_point(aes(alpha = uPrP)) +
        stat_contour() +
            geom_point(aes(x = 20, y = 5, color = "red"))

## Update distribution assuming second destination is (20, 0)
d$searchedDist2 = with(d, searchDistribution(euclideanDistance(x, y, 20, 0)))

ggplot(d, aes(x = x, y = y, z = searchedDist2)) +
    geom_point(aes(alpha = searchedDist2)) +
        stat_contour() +
            geom_point(aes(x = 20, y = 0, color = "red"))

d$uPrP2 = d$uPrP * d$searchedDist2

ggplot(d, aes(x = x, y = y, z = uPrP2)) +
    geom_point(aes(alpha = uPrP2)) +
        stat_contour() +
            geom_point(aes(x = 20, y = 0, color = "red"))

## Function to compute multiple search and update probability
compoundSearchDist = function(data, iter){
    ## searched = dnorm(data$x, 0, sqrt(td)) * dnorm(data$y, 0, sqrt(td))
    searched = rep(1/NROW(data), NROW(data))
    dataCopy = data
    xvec = c()
    yvec = c()
    for(i in 1:iter){
        ## Search with update probability
        x0 = sample(data$x, size = 1, prob = searched)
        xvec = c(xvec, x0)
        y0 = sample(data$y, size = 1, prob = searched)
        yvec = c(yvec, y0)
        print(paste0("searching location (", x0, ", ", y0, ")"))
        searched =
            searched *
                searchDistribution(with(dataCopy, euclideanDistance(x, y, x0, y0)))
    }
    xvec <<- xvec
    yvec <<- yvec
    newDist = dataCopy$PrP * searched
    newDist/sum(newDist)
}

d$updatedSearch = compoundSearchDist(data = d, iter = 100)
d2 = data.frame(x = xvec, y = yvec)


## Use points to denote probability rather than contour, this is much
## more efficient and avoids the problem of non-smooth probability
## polygon.
##
## NOTE (Michael): Should determine the size of the bubble, does it
##                 look better if the bubbles overlap each other?
##
## NOTE (Michael): Want to overlap the points, so it becomes more like
##                 a contour, and at the same time hide the generation
##                 points.
ggplot(d, aes(x = x, y = y, z = updatedSearch)) +
    geom_point(aes(size = updatedSearch, alpha = updatedSearch)) +
    geom_point(data = d2, aes(x = x, y = y, z = 1, col = "red"))

ggplot(d, aes(x = x, y = y, z = updatedSearch)) +
    geom_point(aes(alpha = updatedSearch)) +
    stat_contour() +
    geom_point(data = d2, aes(x = x, y = y, z = 1, col = "red"))


## NOTE (Michael): Need to check the evolution of the density to
##                 determine the right parameters
