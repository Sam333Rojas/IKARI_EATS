let map;

function initMap() {
    var directionsService = new google.maps.DirectionsService;
    var directionsRenderer = new google.maps.DirectionsRenderer;
    map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: 4.7110, lng: -74.0721},
        zoom: 10
    });
    directionsRenderer.setMap(map);
    calculateAndDisplayRoute(directionsService, directionsRenderer);
}

/*
function calculateLocation(address) {
    var geocoder = new google.maps.Geocoder();
    return geocoder.geocode({
        "address": address
    }, function (results) {
        return results[0].geometry.location;
    });
}
*/

function calculateAndDisplayRoute(directionsService, directionsRenderer) {
    directionsService.route({
            origin: {
                lat: 4.5981,
                lng: -74.0760
            },
            destination: {
                lat: 4.6383,
                lng: -74.0885
            },
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
    )
    ;
}

