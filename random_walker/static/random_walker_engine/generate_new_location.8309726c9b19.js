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
				                          'size': map.getSize(),
                                  'n_sample': 5}),
            success: function(data){
		            console.log("successful")
		            if(typeof circle !== 'undefined')
		                map.removeLayer(circle)
                if(typeof routingControl !== 'undefined')
                    map.removeControl(routingControl);
                // Add circle to the destination
                var circle_radius = 300 * Math.pow(2, 13 - map.getZoom())
		            circle = L.geoJson(data, {
			              pointToLayer: function(feature, latlng) {
			                  return new L.circle(latlng, circle_radius, {
                            color: 'red',
                            fillColor: '#f03',
                            fillOpacity: 0.5
                        })
			              }
		            });
		            map.addLayer(circle);


                var new_waypoints = []
                for (i = 0; i < data.features.length; i ++){
                    // var next_point =
                    //     new L.latLng(data.features[i].geometry.coordinates)
                    // new_waypoints.push(next_point)
                    new_waypoints.push(data.features[i].geometry.coordinates)
                }
                var plan = new L.Routing.Plan(new_waypoints)

                var old_waypoints = [
                    L.latLng(home),
                    // L.latLng(data.features[0].geometry.coordinates),
                    // just testing
                    L.latLng(home[0] + Math.random(0.01), home[1] + Math.random(0.01))
                ]

                var plan2 = new L.Routing.Plan(old_waypoints)
                console.log(new_waypoints)
                console.log(old_waypoints)
                console.log(plan)
                console.log(plan2)

                routingControl = L.Routing.control({
                    plan: plan,
                    useZoomParameter: true,
                    show: false,
                    collapsible: false
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
