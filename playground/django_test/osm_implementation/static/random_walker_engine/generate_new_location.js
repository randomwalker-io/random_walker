$(function() {
    $("#newLocationButton").click(function() {
        console.log(map.getBounds().getNorthEast())
        $.ajax({
            url: "{% url 'random_walker_engine:newDestination' %}",
            type: "post",
            dataType: "json",
            // Therse is a problem passing float!
            data: JSON.stringify({'lat': parseFloat(map.getCenter().lat()),
				  'lng': parseFloat(map.getCenter().lng()),
				  'zoom': map.getZoom(),
				  'boundne': map.getBounds().getNorthEast(),
				  'boundsw': map.getBounds().getSouthWest()}),
            success: function(data){
		newDestination = map.getCenter()
		var circle = L.circle(newDestination, 500, {
		    color: 'red',
		    fillColor: '#f03',
		    fillOpacity: 0.5
		}).addTo(map);
            },
            fail: function(data){
		newDestination = map.getCenter()
		var circle = L.circle(newDestination, 500, {
		    color: 'red',
		    fillColor: '#f03',
		    fillOpacity: 0.5
		}).addTo(map);
                alert("failed")
            }
        })
    })
})
