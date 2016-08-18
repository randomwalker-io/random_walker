$(function() {
    $("#getOldLocationButton").on("click touchstart", function() {
	// if data has not been loaded, get it from the database.
	if(typeof previous_locations === 'undefined'){
            $.ajax({
		url: "{% url 'random_walker_engine:showPreviousPoints' %}",
		type: "post",
		dataType: "json",
		data: JSON.stringify(
		    {'username': $.trim($('.dropdown-toggle').text())}
		),
		success: function(data){
		    console.log("successful")
		    previous_locations = new Array();
		    for(var i = 0; i < data.length; i++) {
			var marker  = L.circleMarker(data[i],
						     {
							 color: 'green',
							 fillColor: '#32CD32',
							 fillOpacity: 0.5
						     }).addTo(map);
			map.addLayer(marker);
			previous_locations.push(marker)
		    }
		    previous_location_on = true;
		    $('#getOldLocationButton').text("Hide Previous Locations")
		},
		fail: function(data){
		    console.log("failed")
		}
            })
	} else {
	    //if the data has been loaded, just toggle based on whether it is plotted.
	    if(previous_location_on){
		for(var i = 0; i < previous_locations.length; i++){
		    map.removeLayer(previous_locations[i])
		}
		previous_location_on = false;
		$('#getOldLocationButton').text("Show Previous Locations")
	    } else {
		for(var i = 0; i < previous_locations.length; i++){
		    map.addLayer(previous_locations[i])
		}
		previous_location_on = true;
		$('#getOldLocationButton').text("Hide Previous Locations")
	    }
	}

    })
})
