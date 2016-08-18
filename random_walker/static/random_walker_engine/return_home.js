// Function to return to original location
$(function() {
    $("#returnHomeButton").on("click touchstart", function(){
	map.setView(new L.LatLng(home[0], home[1]), 13)
    })
})
