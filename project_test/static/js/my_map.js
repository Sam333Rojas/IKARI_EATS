var map;

function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
        //lo centramos en el cliente siendo
        center: {lat: client_lat, lng: client_log},
        zoom: 15
    });
    my_routes();
}

var my_routes = function (response, status) {
    calculateAndDisplayRoute(
        {
            lat: dealer_lat,
            lng: dealer_log
        }, {
            lat: res_lat,
            lng: res_log
        });
    calculateAndDisplayRoute(
        {
           lat: res_lat,
            lng: res_log
        }, {
            lat: client_lat,
            lng: client_log
        });
};

function calculateAndDisplayRoute(pointA, pointB) {
    var directionsService = new google.maps.DirectionsService;
    var directionsRenderer = new google.maps.DirectionsRenderer;
    directionsRenderer.setMap(map);
    directionsService.route({
            origin: pointA,
            destination: pointB,
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

