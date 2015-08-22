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
	position: location,
	map: map
    })
    
    // Push the marker to the map
    marker.push(marker);
}
