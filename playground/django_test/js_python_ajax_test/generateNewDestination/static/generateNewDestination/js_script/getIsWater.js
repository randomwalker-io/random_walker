function getIsWater(){
    // Create an in-memory canvas and store its 2d context
    // var water_context = document.createElement('canvas');
    water_context = document.getElementById("water-map");
    water_context.setAttribute('width', 160);
    water_context.setAttribute('height', 160);
    water_context = water_context.getContext('2d');
    // console.log("location is " + param["homeLocation"]['lat'])
    water = new Image();
    water.crossOrigin = 'http://maps.googleapis.com/crossdomain.xml';
    console.log("http://maps.googleapis.com/maps/api/staticmap?scale=2&center=" + param["homeLocation"]['lat'] + "," + param["homeLocation"]['lng'] + "&zoom=" + mapOptions['zoom'] + "&size=160x160&sensor=false&visual_refresh=true&style=element:labels|visibility:off&style=feature:water|color:0x000000&style=feature:transit|visibility:off&style=feature:poi|visibility:off&style=feature:road|visibility:off&style=feature:administrative|visibility:off&key=AIzaSyCYfnPWhBaLjyclMa6KfFdMntt0X5ukndc")
    water.src = "http://maps.googleapis.com/maps/api/staticmap?scale=2&center=" + param["homeLocation"]['lat'] + "," + param["homeLocation"]['lng'] + "&zoom=" + mapOptions['zoom'] + "&size=160x160&sensor=false&visual_refresh=true&style=element:labels|visibility:off&style=feature:water|color:0x000000&style=feature:transit|visibility:off&style=feature:poi|visibility:off&style=feature:road|visibility:off&style=feature:administrative|visibility:off&key=AIzaSyCYfnPWhBaLjyclMa6KfFdMntt0X5ukndc";
    water_context.drawImage(water, 0, 0, 1024, 160);
    console.log(water_context.getImageData(1, 1, 1, 1).data)
}
