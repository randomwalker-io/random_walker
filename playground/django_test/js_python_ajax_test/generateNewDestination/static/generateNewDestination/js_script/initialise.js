function initialize() {
    param = {
        dist: 100000,
        time: Infinity,
	budget: Infinity,
	Purpose: null,
	Distibutrion: 'Normal',
	Confidence: 'Normal'
    }
    //Set home location as Auckland if failed to to geolocate
    homeLocation = new google.maps.LatLng(-36.857992, 174.7621796);

    myZoom = calculateZoom(homeLocation.lat(), param$dist)

    // Need a function to determine zoom
    var mapOptions = {
	zoom: myZoom,
	center: homeLocation
    }

    map = new google.maps.Map(document.getElementById('map'),  
			      mapOptions);
    // map.fitBounds(myBounds)

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
}

function addMarker(location) {
    var mapOptions = {
    	zoom: 7,
    	center: homeLocation
    };

    // Access the map object 
    var map = new google.maps.Map(document.getElementById("map"), 
				  mapOptions);
    
    // Create the marker
    var marker = new google.maps.Marker({
	position: location,
	map: map
    })
    
    // Push the marker to the map
    marker.push(marker);
}
