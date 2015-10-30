
########################################################################
## Title: Spatial point analysis
## Date: 2015-10-28
########################################################################

## Set up the grid

createDensityMatrix = function(index, nrow = 100, ncol = 100){
    x = rep(1:nrow, ncol)
    y = rep(1:ncol, each = nrow)
    d = sqrt((x - index[1])^2 + (y - index[2])^2)
    dmat = matrix(d, nrow = nrow, ncol = ncol, byrow = FALSE)
    ds = sqrt((nrow/2)^2 + (ncol/2)^2)/10
    pmat = dnorm(dmat, mean = 0, sd = ds)
    pmat/sum(pmat)
}
test = createDensityMatrix(index = c(20, 50), 100, 200)

test1 = function(n, ncol = 100, nrow = 100){
    base = matrix(10000, nrow = nrow, ncol = ncol)
    for(i in 1:n){
        learning = createDensityMatrix(c(sample(nrow, 1), sample(ncol, 1)),
                                       nrow = nrow, ncol = ncol)
        base = base * (1 - learning)
    }
    base/sum(base)
}

system.time({r1 = test1(100, 100, 100)})
image(r1)


dimx = 100
dimy = 100
posx = runif(100, 0, 100)
posy = runif(100, 0, 100)
## posx = rnorm(100, 50, 10)
## posy = rnorm(100, 50, 10)
gridx = rep(1:dimx, dimy)
gridy = rep(1:dimy, each = dimx)

kernel2d = function(center, posx, posy, bandx = 1, bandy = 1){
    1/(2 * pi * bandx * bandy) *
        exp(-0.5 * ((posx - center[1])/bandx)^2 -0.5 * ((posy - center[2])/bandy)^2)
}



computeKernel = function(gridx, gridy, posx, posy){
    FUN = function(gx, gy){
        ## print(c(gx, gy))
        kernel2d(c(gx, gy), posx, posy)
    }
    matrix(mapply(FUN, gx = gridx, gy = gridy), nrow = max(gridx), ncol = max(gridy))
}

test = computeKernel(gridx, gridy, posx, posy)
image(test)
points(posx/100, posy/100, pch = 19)

plot(posx, posy, pch = 19)
image(test, add = TRUE)

library(MASS)

with(geyser,
     {
         plot(duration, waiting, xlim = c(0.5,6), ylim = c(40,100))
         f1 = kde2d(duration, waiting, n = 50, lims = c(0.5, 6, 40, 100))
         image(f1, zlim = c(0, 0.05))
         f2 = kde2d(duration, waiting, n = 50, lims = c(0.5, 6, 40, 100),
             h = c(width.SJ(duration), width.SJ(waiting)) )
         image(f2, zlim = c(0, 0.05))
     })

f3 = kde2d(posx, posy, n = 100, lims = c(0, 100, 0, 100))
image(f3)


final = r1 * f3$z/sum(f3$z)
## final = final/sum(final)
par(mfrow = c(1, 3))
image(r1)
image(f3)
image(final)

zr = range(c(r1, f3$z))

persp(r1, zlim = zr)
persp(f3, zlim = zr)
persp(final, zlim = zr)



########################################################################
## Title: Function to calculate bandwidth based on lat long for fix
##        distance
## Date: 2015-10-29
########################################################################


er = 3960
d2r = pi/180
r2d = 180/pi

calcBandLng = function(lat, d){
    r = er * cos(lat * d2r)
    d/r * r2d
}

calcBandLat = function(d){
    d/er * r2d
}

calcBandLng(0, 0.2)
calcBandLat(0.2)

calcBandLng(80, 0.2)
calcBandLat(0.2)

library(XML)
map = xmlParse("map.osm")
map.lst = xmlToList(map)

## Select only nodes
mapNodes.lst = map.lst[which(names(map.lst) == "node")]

## 
hasList = sapply(mapNodes.lst, FUN = function(x) is.list(x))
mapTag.lst = mapNodes.lst[hasList]



## This is the successful implementation of the cafe density. Need to
## check how to download all the nodes
map = xmlParse("city.osm")
map.lst = xmlToList(map)
mapNodes.lst = map.lst[which(names(map.lst) == "node")]

hasList = sapply(mapNodes.lst, FUN = function(x) is.list(x))
mapTag.lst = mapNodes.lst[which(hasList)]
## isCafe = sapply(mapTag.lst,
##     FUN = function(x) x$tag["v"] == "cafe")
## isCafe = sapply(mapTag.lst,
##     FUN = function(x) x$tag["k"] == "amenity" &
##         x$tag["v"] %in% c("cafe", "restaurant", "fast_food"))
isCafe = sapply(mapTag.lst,
    FUN = function(x) x$tag["k"] == "amenity")
mapCafe.lst = mapTag.lst[which(isCafe)]

cafeLoc = sapply(mapCafe.lst, FUN = function(x) as.numeric(x$`.attrs`[c("lat", "lon")]))
cafeName = sapply(mapCafe.lst, FUN = function(x) x[[2]]["v"])
plot(cafeLoc[2, ], cafeLoc[1, ])
text(cafeLoc[2, ], cafeLoc[1, ], labels = cafeName)

latLonDim = as.numeric(map.lst[["bounds"]])

## Get map center
mapCenter = c(latLonDim[2] + diff(latLonDim[c(2, 4)])/2,
    latLonDim[1] + diff(latLonDim[c(1, 3)])/2)

## set bandwidth as 100 meters, which is an assumed walking search distance
bandLng = calcBandLng(mapCenter[2], 100/1000)
bandLat = calcBandLat(100/1000)

cafeDen = kde2d(cafeLoc[2, ], cafeLoc[1, ], n = 300,
    lims = c(latLonDim[c(2, 4)], latLonDim[c(1, 3)]),
    h = c(bandLng, bandLat))
image(cafeDen)
points(cafeLoc[2, ], cafeLoc[1, ], pch = 19)






## This is the successful implementation of the cafe density. Need to
## check how to download all the nodes
map = xmlParse("akl_cbd.osm")
map.lst = xmlToList(map)
mapNodes.lst = map.lst[which(names(map.lst) == "node")]

hasList = sapply(mapNodes.lst, FUN = function(x) is.list(x))
mapTag.lst = mapNodes.lst[which(hasList)]
isCafe = sapply(mapTag.lst,
    FUN = function(x) x$tag["k"] == "amenity")
mapCafe.lst = mapTag.lst[which(isCafe)]

cafeLoc = sapply(mapCafe.lst, FUN = function(x) as.numeric(x$`.attrs`[c("lat", "lon")]))
cafeName = sapply(mapCafe.lst, FUN = function(x) x[[2]]["v"])
plot(cafeLoc[2, ], cafeLoc[1, ])
text(cafeLoc[2, ], cafeLoc[1, ], labels = cafeName)

latLonDim = as.numeric(map.lst[["bounds"]])

## Get map center
mapCenter = c(latLonDim[2] + diff(latLonDim[c(2, 4)])/2,
    latLonDim[1] + diff(latLonDim[c(1, 3)])/2)

## set bandwidth as 100 meters, which is an assumed walking search distance
bandLng = calcBandLng(mapCenter[2], 0.5)
bandLat = calcBandLat(0.5)

cafeDen = kde2d(cafeLoc[2, ], cafeLoc[1, ], n = 300,
    lims = c(latLonDim[c(2, 4)], latLonDim[c(1, 3)]),
    h = c(bandLng, bandLat))
image(cafeDen)
points(cafeLoc[2, ], cafeLoc[1, ], pch = 19)




map = xmlParse("quito_cbd.osm")
map.lst = xmlToList(map)
mapNodes.lst = map.lst[which(names(map.lst) == "node")]

hasList = sapply(mapNodes.lst, FUN = function(x) is.list(x))
mapTag.lst = mapNodes.lst[which(hasList)]
isCafe = sapply(mapTag.lst,
    FUN = function(x) x$tag["k"] == "amenity")
mapCafe.lst = mapTag.lst[which(isCafe)]

cafeLoc = sapply(mapCafe.lst, FUN = function(x) as.numeric(x$`.attrs`[c("lat", "lon")]))
cafeName = sapply(mapCafe.lst, FUN = function(x) x[[2]]["v"])
plot(cafeLoc[2, ], cafeLoc[1, ])
text(cafeLoc[2, ], cafeLoc[1, ], labels = cafeName)

latLonDim = as.numeric(map.lst[["bounds"]])

## Get map center
mapCenter = c(latLonDim[2] + diff(latLonDim[c(2, 4)])/2,
    latLonDim[1] + diff(latLonDim[c(1, 3)])/2)

## set bandwidth as 100 meters, which is an assumed walking search distance
bandLng = calcBandLng(mapCenter[2], 0.5)
bandLat = calcBandLat(0.5)

cafeDen = kde2d(cafeLoc[2, ], cafeLoc[1, ], n = 300,
    lims = c(latLonDim[c(2, 4)], latLonDim[c(1, 3)]),
    h = c(bandLng, bandLat))
image(cafeDen)
points(cafeLoc[2, ], cafeLoc[1, ], pch = 19)




map = xmlParse("quito.osm")
map.lst = xmlToList(map)
mapNodes.lst = map.lst[which(names(map.lst) == "node")]

hasList = sapply(mapNodes.lst, FUN = function(x) is.list(x))
mapTag.lst = mapNodes.lst[which(hasList)]
isCafe = sapply(mapTag.lst,
    FUN = function(x) x$tag["k"] == "amenity")
mapCafe.lst = mapTag.lst[which(isCafe)]

cafeLoc = sapply(mapCafe.lst, FUN = function(x) as.numeric(x$`.attrs`[c("lat", "lon")]))
cafeName = sapply(mapCafe.lst, FUN = function(x) x[[2]]["v"])
plot(cafeLoc[2, ], cafeLoc[1, ])
text(cafeLoc[2, ], cafeLoc[1, ], labels = cafeName)

latLonDim = as.numeric(map.lst[["bounds"]])

## Get map center
mapCenter = c(latLonDim[2] + diff(latLonDim[c(2, 4)])/2,
    latLonDim[1] + diff(latLonDim[c(1, 3)])/2)

## set bandwidth as 100 meters, which is an assumed walking search distance
bandLng = calcBandLng(mapCenter[2], 5)
bandLat = calcBandLat(5)

cafeDen = kde2d(cafeLoc[2, ], cafeLoc[1, ], n = 300,
    lims = c(latLonDim[c(2, 4)], latLonDim[c(1, 3)]),
    h = c(bandLng, bandLat))
image(cafeDen)
points(cafeLoc[2, ], cafeLoc[1, ], pch =".")



den.df = with(cafeDen, expand.grid(x, y))
den.df$val = c(cafeDen$z)
library(ggplot2)
ggplot(data = den.df, aes(x = Var1, y = Var2, fill = val)) +
    geom_tile() +
    geom_point(aes(x = lat, y = lng, fill = NULL), data = cafeLoc.df)
