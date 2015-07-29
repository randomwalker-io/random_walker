function addMarker(location) {
    var marker = new google.maps.Marker({
	position: location,
	map: map
    });
    markers.push(marker);
}
