$(function() {
    $("#getOldLocationButton").on("click touchstart", function() {
        console.log(map.getBounds().getNorthEast())
        $.ajax({
            url: "{% url 'random_walker_engine:showPreviousPoints' %}",
            type: "post",
            dataType: "json",
            data: JSON.stringify({'username': $.trim($('.dropdown-toggle').text())}),
            success: function(data){
		console.log("successful")
		for (var i = 0; i < data.length; i++) {
		    console.log(data[i]);
		    marker = L.circleMarker(data[i],
					    {
						color: 'green',
						fillColor: '#32CD32',
						fillOpacity: 0.5
					    }).addTo(map);
		}
            },
            fail: function(data){
		console.log("failed")
            }
        })
    })
})
