//Client
/*
se conecta con active_purchase.html
genera la orden con los datos del cliente y del restaurante
recibe la orden con datos del dealer
muestra los puntos y recorrido
muestra tiempo total de recorrido
*/

let map;
//let client_lat; let client_log;
function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
        // lo centramos en el dealer siendo
        // center: {lat: client_lat, lng: client_long},
        center: {lat: 4.7110, lng: -74.0721},
        zoom: 10
    });
    navigator.geolocation.getCurrentPosition(geoSuccess, geoError);
    // en lugar de marker1 , marker2 , marker 4 usamos destinations en current_order.html
/*
    for(var i=0;i< destinations.length; i++) {
    var marker = new google.maps.Marker({
        position: destinations.get(i),
        map: map,
        title: 'Hello World!'
    });
    }
*/
    var marker1 = new google.maps.Marker({
        position: {lat: 4.5981, lng: -75.0760},
        map: map,
        title: 'Hello World!'
    });

    var marker2 = new google.maps.Marker({
        position: {lat: 4.4521, lng: -74.0760},
        map: map,
        title: 'Hello World!'
    });

    var marker4 = new google.maps.Marker({
        position: {lat: 4.5981, lng: -77.0760},
        map: map,
        title: 'Hello World!'
    });
}

function calculateAndDisplayRoute(pointA, pointB) {
    var directionsService = new google.maps.DirectionsService;
    var directionsRenderer = new google.maps.DirectionsRenderer;
    directionsRenderer.setMap(map);
    directionsService.route({
            origin: pointA,
            destination: pointB,
            // travelMode:
            // 'BIKING'
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

//muestra la posicion actual del dealer
//falta enviar esa posicion a la orden
let geoSuccess = function (position) {
    startPos = position;
    // console.log(position);
    // user_lat = position.coords.latitude ;user_lat = position.coords.longitude ;
    var marker = new google.maps.Marker({
        position: {lat: position.coords.latitude, lng: position.coords.longitude},
        map: map,
        title: 'Hello World!'
    });
};
let geoError = function (error) {
    switch (error.code) {
        case error.TIMEOUT:
            console.log('error');
            break;
    }
};
