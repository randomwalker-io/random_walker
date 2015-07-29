function generateDestination(){
    var mapOptions = {
    	zoom: 7,
    	center: homeLocation
    };
    var radius = 2;
    // cretate shift
    var angle = Math.random() * 2 * Math.PI;
    var latShift = Math.cos(angle) * radius;
    var lngShift = Math.sin(angle) * radius;

    // Add shift to the original location
    var newLat = mapOptions.center.lat() + latShift;
    var newLng = mapOptions.center.lng() + lngShift;

    // Create the new LatLng object
    var newDestination = new google.maps.LatLng(newLat, newLng);
    return newDestination;
};


