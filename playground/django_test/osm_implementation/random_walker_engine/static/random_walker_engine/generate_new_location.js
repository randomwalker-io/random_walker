$(function() {
    $("#newLocationButton").click(function() {
        console.log(map.getBounds().getNorthEast())
        $.ajax({
            url: "{% url 'random_walker_engine:newDestination' %}",
            type: "post",
            dataType: "json",
            data: JSON.stringify({'lat': parseFloat(map.getCenter()['lat']),
				  'lng': parseFloat(map.getCenter()['lng']),
				  'zoom': map.getZoom(),
				  'boundne': map.getBounds().getNorthEast(),
				  'boundsw': map.getBounds().getSouthWest(),
				  'size': map.getSize()}),
            success: function(data){
		console.log("successful")
		var circle = L.circle(data, 500, {
		    color: 'red',
		    fillColor: '#f03',
		    fillOpacity: 0.5
		}).addTo(map);
            },
            fail: function(data){
		console.log("failed")
            }
        })
    })
})
