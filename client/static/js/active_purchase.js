  var directionDisplay;
  var map;

  function initMap() {
    directionsDisplay = new google.maps.DirectionsRenderer();
    var center = new google.maps.LatLng(client_lat, client_log);
    var myOptions = {
      zoom: 15,
      mapTypeId: google.maps.MapTypeId.ROADMAP,
      center: center
    }
    map = new google.maps.Map(document.getElementById("map"), myOptions);
    directionsDisplay.setMap(map);
    calcRoute();
     var rest_str = ''.concat(res_lat,',',res_log);
    var marker = new google.maps.Marker({
    position: rest_str,
    map: map
});
  }
  
  function calcRoute() {
    var origin_str = ''.concat(client_lat,',',client_log);
      var destination_str = ''.concat(dealer_lat,',',dealer_log);
      var waypoint_str = ''.concat(res_lat,',',res_log);
    var request = {
        origin: origin_str,
        destination: destination_str,
        waypoints: [{
          location: waypoint_str,
          stopover:true}],
        optimizeWaypoints: true,
        travelMode: google.maps.DirectionsTravelMode.DRIVING
    };
      var directionsService = new google.maps.DirectionsService();
    directionsService.route(request, function(response, status) {
      if (status === google.maps.DirectionsStatus.OK) {
        directionsDisplay.setDirections(response);
        var route = response.routes[0];
        var summaryPanel = document.getElementById("directions_panel");
        summaryPanel.innerHTML = "";
        computeTotalDistance(response);
      } else {
        alert("directions response "+status);
      }
    });
  }

   function computeTotalDistance(result) {
      var totalDist = 0;
      var totalTime = 0;
      var myroute = result.routes[0];
      for (i = 0; i < myroute.legs.length; i++) {
        totalDist += myroute.legs[i].distance.value;
        totalTime += myroute.legs[i].duration.value;
      }
      totalDist = totalDist / 1000.
      document.getElementById("total").innerHTML = "Dis is: "+ totalDist + " km<br>Time is: " + (totalTime / 60).toFixed(2) + " mins";
      }