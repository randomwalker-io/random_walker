$(function() {
    $("#getOldLocationButton").on("click touchstart", function() {
        console.log(map.getBounds().getNorthEast())
	if(typeof previous_marker !== 'undefined'){
	    map.removeLayer(previous_marker)
	} else {
            $.ajax({
		url: "{% url 'random_walker_engine:showPreviousPoints' %}",
		type: "post",
		dataType: "json",
		data: JSON.stringify({'username': $.trim($('.dropdown-toggle').text())}),
		success: function(data){
		    console.log("successful")
		    for (var i = 0; i < data.length; i++) {
			previous_marker = L.circleMarker(data[i],
							 {
							     color: 'green',
							     fillColor: '#32CD32',
							     fillOpacity: 0.5
							 }).addTo(map);
		    }
		    $("#getOldLocationButton").text("Hide Previous Locations")
		},
		fail: function(data){
		    console.log("failed")
		}
            })
	}
    })
})
