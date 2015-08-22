function initialize() {
    //Set home location as Auckland if failed to to geolocate
    homeLocation = new google.maps.LatLng(-36.857992, 174.7621796);
    //Set home location to central china to avoid non possible location;
    // homeLocation = new google.maps.LatLng(25.9227467, 91.9315795); 

    // First generate the new destination
    newDestination = generateDestination();
    
    var mapOptions = {
	zoom: 8,
	center: homeLocation
    }
    map = new google.maps.Map(document.getElementById('map-canvas'),  
			      mapOptions);

    // Create the search box and link it to the UI element.
    var input = /** @type {HTMLInputElement} */(
	document.getElementById('pac-input'));
    map.controls[google.maps.ControlPosition.TOP_LEFT].push(input);

    var searchBox = new google.maps.places.SearchBox(
	/** @type {HTMLInputElement} */(input));

    geocoder = new google.maps.Geocoder();
    google.maps.event.addListener(searchBox, 'places_changed', function() {
	var places = searchBox.getPlaces();
	console.log(places[0].formatted_address);
	if (places.length == 0) {
	    return;
	} else {
	    enterHomeAddress(places[0].formatted_address);
	}
    });


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
    	}, function() {
    	    handleNoGeolocation(true);
    	});
    } else {
    	// Browser doesn't support Geolocation
    	handleNoGeolocation(false);
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
    };
    calcRoute();
    directionsDisplay.setMap(map);
}
