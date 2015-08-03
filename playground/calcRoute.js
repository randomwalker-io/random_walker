function calcRoute() {
    var start = homeLocation;
    var end = newDestination;
    var request = {
	origin:start,
	destination:end,
	travelMode: google.maps.TravelMode.DRIVING
    };
    directionsService.route(request, function(response, status) {
	console.log(status);
	if (status == google.maps.DirectionsStatus.OK) {
	    directionsDisplay.setDirections(response);

	} else {
	    if (status == google.maps.DirectionsStatus.OVER_QUERY_LIMIT){
		window.alert(status);
		// Should we change the setting?
	    } else {
		generateDestination();
		calcRoute();
	    }
	}
    });
}
