var map;
var time;
function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: dealer_lat, lng: dealer_log},
        zoom: 10
    });
    var service = new google.maps.DistanceMatrixService();
    service.getDistanceMatrix(
        {
            origins: [{lat: dealer_lat, lng: dealer_log}],
            destinations: [{lat: client_lat, lng: client_log}],
            travelMode: 'DRIVING',
            avoidHighways: false,
            avoidTolls: false
        }, callbackMatrix);
}
var callbackMatrix = function (response, status) {
    console.log(response);
    var min = response.rows[0].elements[0].duration.value, minIndex = 0;

    for (var i = 1; i < response.rows[0].elements.length; i++) {
        if (min > response.rows[0].elements[i].duration.value) {
            min = response.rows[0].elements[i].duration.value;
            minIndex = i;
        }
    }
    calculateAndDisplayRoute({
        lat: dealer_lat,
        lng: dealer_log
    }, response.destinationAddresses[minIndex]);
};

function calculateAndDisplayRoute(pointA, pointB) {
    var directionsService = new google.maps.DirectionsService;
    var directionsRenderer = new google.maps.DirectionsRenderer;
    var waypoint_str = ''.concat(res_lat, ',', res_log);
    directionsRenderer.setMap(map);
    directionsService.route({
            origin: pointA,
            destination: pointB,
            waypoints: [{
                location: waypoint_str,
                stopover: true
            }],
            travelMode:
                'DRIVING'
        },

        function (response, status) {
            if (status === 'OK') {
                directionsRenderer.setDirections(response);
            } else {
                window.alert('Directions request failed due to ' + status);
            }
        }
    );
}