function initialise() {
    // Default parameters
    param = {
	//Set home location as Auckland if failed to to geolocate
	homeLocation: {'lat': -36.857992, 'lng': 174.7621796},
        dist: 100000,
        time: Infinity,
	budget: Infinity,
	Purpose: null,
	Distribution: 'Normal',
	Confidence: 'Normal'
    }
    console.log(param["homeLocation"]["lat"] + "," + param["homeLocation"]["lng"])
    // homeLocation = new google.maps.LatLng(-36.857992, 174.7621796);
    homeLocation = new google.maps.LatLng(param['homeLocation']['lat'], 
					  param['homeLocation']['lng'])

    // Calculate the
    myZoom = calculateZoom(homeLocation.lat(), param['dist'])

    // Need a function to determine zoom
    mapOptions = {
	zoom: myZoom,
	center: homeLocation
    }

    map = new google.maps.Map(document.getElementById('map'),  
			      mapOptions);

    // Try HTML5 geolocation
    if(navigator.geolocation) {
    	navigator.geolocation.getCurrentPosition(function(position) {
	    //Update the parameter
	    param['homeLocation']['lat'] = position.coords.latitude
	    param['homeLocation']['lng'] = position.coords.longitude

	    //Update the homelocation
    	    homeLocation = new google.maps.LatLng(position.coords.latitude,
    						  position.coords.longitude);
	    mapOptions = {
		zoom: myZoom,
		center: homeLocation
	    }
	    
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
    // getIsWater();

    map.addListener('bounds_changed', function(){
	homeLocation = map.getCenter()
	param["homeLocation"]["lat"] = newCenter.lat()
	param["homeLocation"]["lng"] = newCenter.lng()
	map.setCenter(homeLocation)
    })

    map.addListener('center_changed', function(){
	homeLocation = map.getCenter()
	param["homeLocation"]["lat"] = newCenter.lat()
	param["homeLocation"]["lng"] = newCenter.lng()
	map.setCenter(homeLocation)
    })


    map.addListener('zoom_changed', function(){
	mapOptions = {
	    zoom: map.getZoom(),
	    center: homeLocation
	}
    })
	
}

