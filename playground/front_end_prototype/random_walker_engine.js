var map = L.map('map').setView([51.505, -0.09], 10);

// // add an OpenStreetMap tile layer
// L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
//     attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
// }).addTo(map);

// Mapbox tile layer
L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
    attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
    maxZoom: 18,
    id: 'mkao006.cierjexrn01naw0kmftpx3z1h',
    accessToken: 'pk.eyJ1IjoibWthbzAwNiIsImEiOiJjaWVyamV5MnkwMXFtOXRrdHRwdGw4cTd0In0.H28itS1jvRgLZI3JhirtZg'
}).addTo(map);
