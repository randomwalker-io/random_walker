function addMarker(location) {
    // Create the marker
    var marker = new google.maps.Marker({
	position: location,
	map: map // The map is assumed created already.
    })
}
