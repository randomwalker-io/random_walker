function generateDestination(){
    console.log('generateDestination called');
    console.log(homeLocation);
    var tmp = JSON.stringify({'current_location': {lat: 2.2, lng: 1.1}})
    console.log(tmp);
    

    $.ajax({
        url : "/static/random_walker_py/generateDestination.py", // the endpoint
	// url: "generateDestination/",
        type : "POST", // http method
	// dataType: "json",
	// data: homeLocation,
        data : JSON.stringify(homeLocation),

        // handle a successful response
        success : function(json) {
            console.log(json); // log the returned json to the console
            // console.log("success"); // another sanity check
	    newDestination = new google.maps.LatLng(json);
	    // newDestination = new google.maps.LatLng(homeLocation.lat() + 0.1, homeLocation.lng() + Math.random() * 0.1)
	    codeLatLng();
	    calcRoute();
	    directionsDisplay.setMap(map);
        },
	error: function(xhr,errmsg,err) {
	    console.log(errmsg);
	    console.log(xhr.responseText);
	}
    })
}
	


// function generateDestination(){
//     var radius = 0.2;
//     // cretate shift, angle is in radian
//     var angle = Math.random() * 2 * Math.PI;
//     var latShift = Math.cos(angle) * radius;
//     var lngShift = Math.sin(angle) * radius;

//     // Add shift to the original location
//     // var newLat = mapOptions.center.lat() + latShift;
//     // var newLng = mapOptions.center.lng() + lngShift;
//     var newLat = homeLocation.lat() + latShift;
//     var newLng = homeLocation.lng() + lngShift;

//     // Create the new LatLng object
//     newDestination = new google.maps.LatLng(newLat, newLng);
//     return newDestination
// };


