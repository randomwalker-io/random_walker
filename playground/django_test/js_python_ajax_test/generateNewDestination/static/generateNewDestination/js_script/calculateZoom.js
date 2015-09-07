/*
function to estimate the require zoom given the possible generation
distance.

source:https://groups.google.com/forum/#!topic/google-maps-js-api-v3/hDRO4oHVSeM

NOTE: Need to also adjust for the restricted window!
*/


function calculateZoom(lat, dist){
    var radiusEarth = 6378137
    var k = radiusEarth * 2 * Math.PI/256
    var desireRes = dist/256
    var desireZoom = Math.ceil((Math.log(desireRes) - Math.log(Math.cos(lat * Math.PI/180) * k))/-Math.log(2))

    return desireZoom
}
