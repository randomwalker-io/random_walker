function addMarker(location) {
    var mapOptions = {
	zoom: 7,
	center: homeLocation
    };
    // Access the map object
    var map = new google.maps.Map(document.getElementById("map-canvas"), 
				  mapOptions);

    // Create the marker
    var marker = new google.maps.Marker({
	position: location
    });
    
    //Set the marker on the map
    marker.setMap(map);
}
