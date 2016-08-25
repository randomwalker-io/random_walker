// Initialisation of the Random Walker Engine

// The get current location code is from: http://themarklee.com/2013/10/27/super-simple-geolocation/

// call getCurrentPosition()
if('geolocation' in navigator){
    navigator.geolocation.getCurrentPosition(success, error, options);
} else {
    // Initialise location at Auckland
    home = [-36.85764758564406, 174.76226806640625]
    initialise(home);
}

var options = {
    // enableHighAccuracy = should the device take extra time or power to return a really accurate result, or should it give you the quick (but less accurate) answer?
    enableHighAccuracy: true,
    // timeout = how long does the device have, in milliseconds to return a result?
    timeout: 5000,
    // maximumAge = maximum age for a possible previously-cached position. 0 = must return the current position, not a prior cached position
    maximumAge: 0
};


// upon success, do this
function success(pos){
    // get longitude and latitude from the position object passed in
    var lng = pos.coords.longitude;
    var lat = pos.coords.latitude;
    // and presto, we have the device's location! Let's just alert it for now...
    console.log("You appear to be at longitude: " + lng + " and latitude: " + lat);
    // Initialise the map at the user location
    home = [lat, lng]
    initialise(home);
}

// upon error, do this
function error(err){
    // Initialise location at Auckland
    home = [-36.85764758564406, 174.76226806640625]
    initialise(home);
}



function initialise(pos){
    // Setting the width and height of the map element. Although not
    // the best practice it helps to make sure the size is valid

    // set the width and height accodring to device
    if(isMobile()){
	      width = Math.min(1280, $(window).width())
	      height = $(document).height() - $('#nav_bar').outerHeight(true) -
	          $('.engine_control').outerHeight(true)
    } else {
	      width = Math.min(1280, $(window).width())
	      height = Math.min(width * 9/16, $(document).height() -
			                    $('#nav_bar').outerHeight(true) -
			                    $('.engine_control').outerHeight(true))
    }

    // initialise the map
    $('#map').height(height).width(width);
    map = L.map('map', {
	      center: pos,
    	  zoom: 13,
	      minZoom: 2
    });
    // Add the tiles to the map
    L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
	      attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
	      tileSize: 256
    }).addTo(map);


    // L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
    // 	attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
    // 	id: 'mkao006.cierjexrn01naw0kmftpx3z1h',
    // 	accessToken: 'pk.eyJ1IjoibWthbzAwNiIsImEiOiJjaWVyamV5MnkwMXFtOXRrdHRwdGw4cTd0In0.H28itS1jvRgLZI3JhirtZg',
    // 	tileSize: 256
    // }).addTo(map);

    // Add the marker of the user location
    marker = L.marker(pos, {
	      draggable: true,
	      opacity: 0.8
    }).addTo(map)
	      .bindPopup('Drag the marker to your current location!')
	      .openPopup()
	      .on('dragend', function(e) {console.log('location changed');
				                            map.setView(marker.getLatLng());
				                           });
}
