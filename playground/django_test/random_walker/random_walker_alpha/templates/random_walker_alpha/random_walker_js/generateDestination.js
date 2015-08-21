function generateDestination(){
    var radius = 0.2;
    // cretate shift, angle is in radian
    var angle = Math.random() * 2 * Math.PI;
    var latShift = Math.cos(angle) * radius;
    var lngShift = Math.sin(angle) * radius;

    // Add shift to the original location
    // var newLat = mapOptions.center.lat() + latShift;
    // var newLng = mapOptions.center.lng() + lngShift;
    var newLat = homeLocation.lat() + latShift;
    var newLng = homeLocation.lng() + lngShift;

    // Create the new LatLng object
    newDestination = new google.maps.LatLng(newLat, newLng);
    return newDestination
};


