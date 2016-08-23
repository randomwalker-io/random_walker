// Function to generate a new destination
$(function() {
    $("#newLocationButton").on("click touchstart", function() {
	      $("#newLocationButton")
            .removeClass('btn-success')
            .addClass('btn-danger')
            .text('Generating Location!')
        $.ajax({
            // url: "{% url 'random_walker_engine:generate_new_destination' %}",
            url : "random_walker_engine:generate_new_destination",
            type: "POST",
            dataType: "json",
            data: JSON.stringify({'lat': parseFloat(map.getCenter()['lat']),
				                          'lng': parseFloat(map.getCenter()['lng']),
				                          'zoom': map.getZoom(),
				                          'boundne': map.getBounds().getNorthEast(),
				                          'boundsw': map.getBounds().getSouthWest(),
				                          'size': map.getSize()}),
            success: function(data){
		            console.log("successful")
		            if(typeof circle !== 'undefined')
		                map.removeLayer(circle)
                // Add circle to the destination
		            circle = L.circle(data,
				                          500 * Math.pow(2, 13 - map.getZoom()),
				                          {
				                              color: 'red',
				                              fillColor: '#f03',
				                              fillOpacity: 0.5
				                          }).addTo(map);

                // Add routing from home to the destination.
                console.log(data)
                console.log(marker.getLatLng())
                current = marker.getLatLng();
                var plan = new L.Routing.Plan([
                    L.latLng(home),
                    L.latLng(data),
                    // Just testing
                    L.latLng(home[0] + Math.random(0.01), home[1] + Math.random(0.01))
                ])
                L.Routing.control({
                    plan: plan,
                    useZoomParameter: true
                }).addTo(map);
		            $("#newLocationButton")
                    .addClass('btn-success')
                    .removeClass('btn-danger')
                    .text('Give Me A New Location!')
            },
            fail: function(data){
		            console.log("failed")
		            $("#newLocationButton")
                    .addClass('btn-success')
                    .removeClass('btn-danger')
                    .text('Give Me A New Location!')
            }
        })
    })
})
