function enterHomeAddress(address) {
    geocoder.geocode( { 'address': address}, function(results, status) {
	console.log(status);
	if (status == google.maps.GeocoderStatus.OK) {
	    console.log(results[0].geometry.location);
	    homeLocation = results[0].geometry.location
	    map.setCenter(homeLocation);
	}
    })
};
