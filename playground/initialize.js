function initialize() {
    //Set home location as Auckland if failed to to geolocate
    homeLocation = new google.maps.LatLng(-36.857992, 174.7621796);
    
    var mapOptions = {
	zoom: 8,
	center: homeLocation
    }
    var map = new google.maps.Map(document.getElementById('map-canvas'),  
				  mapOptions);

    // Try HTML5 geolocation
    if(navigator.geolocation) {
    	navigator.geolocation.getCurrentPosition(function(position) {
    	    homeLocation = new google.maps.LatLng(position.coords.latitude,
    						  position.coords.longitude);
	    
    	    var infowindow = new google.maps.InfoWindow({
    		map: map,
    		position: homeLocation,
    		content: 'Location found using HTML5.'
    	    });
	    
    	    map.setCenter(homeLocation);
	    generateDestination();
    	}, function() {
    	    handleNoGeolocation(true);
	    generateDestination();
    	});
    } else {
    	// Browser doesn't support Geolocation
    	handleNoGeolocation(false);
	generateDestination();
    }

    function handleNoGeolocation(errorFlag) {
    	if (errorFlag) {
    	    var content = 'Error: The Geolocation service failed.';
    	} else {
    	    var content = 'Error: Your browser doesn\'t support geolocation.';
    	}
    	var options = {
    	    map: map,
    	    position: homeLocation,
    	    content: content
    	};

    	var infowindow = new google.maps.InfoWindow(options);
    	map.setCenter(options.position);
	generateDestination();
    };
   

}

