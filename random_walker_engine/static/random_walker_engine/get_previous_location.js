// Function to display and toggle previous locations
$(function() {
    $("#getOldLocationButton").on("click touchstart", function() {
	// if data has not been loaded, get it from the database.
	if(typeof geojsonLayer === 'undefined'){
            $.ajax({
		url: "{% url 'random_walker_engine:showPreviousPoints' %}",
		type: "get",
		dataType: "json",
		data: JSON.stringify(
		    {'username': $.trim($('.dropdown-toggle').text())}
		),
		success: function(data){
		    console.log("successful")
		    geojsonLayer = L.geoJson(data, {
			pointToLayer: function(feature, latlng) {
			    return new L.CircleMarker(latlng, {
				color: 'green',
                                fillColor: '#32CD32',
                                fillOpacity: 0.5
                            })
			}
		    });
		    map.addLayer(geojsonLayer);
		    $('#getOldLocationButton').text("Hide Previous Locations")
		    previous_location_on = true
		},
		fail: function(data){
		    console.log("failed")
		}
            })
	} else {
	    //if the data has been loaded, just toggle based on
	    //whether it is plotted.
	    if(previous_location_on){
		map.removeLayer(geojsonLayer);
		previous_location_on = false;
		$('#getOldLocationButton').text("Show Previous Locations")
	    } else {
		map.addLayer(geojsonLayer);
		previous_location_on = true;
		$('#getOldLocationButton').text("Hide Previous Locations")
	    }
	}

    })
})
