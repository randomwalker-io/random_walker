function codeLatLng() {
    var latlng = newDestination
    geocoder.geocode({'location': latlng}, function(results, status) {
	if (status == google.maps.GeocoderStatus.OK) {
	    if (results[0]) {
		// overwrite the new destination with reverse geocoding.
		newDestination = results[0].formatted_address;
		console.log(newDestination);
	    }
	}})
};
