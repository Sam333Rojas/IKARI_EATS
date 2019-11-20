//Dealer
/*
calcula la ruta entre el y el restaurante
envia el tiempo correspondiente
si es aceptado traza la ruta entre el y el restaurante
si es aceptado cambia su status y lo envia por post
 */

let map;
//let dealer_lat;let dealer_log;
function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
        //lo centramos en el dealer siendo
        // center: {lat: dealer_lat, lng: dealer_long},
        center: {lat: 4.7110, lng: -74.0721},
        zoom: 10
    });
    navigator.geolocation.getCurrentPosition(geoSuccess, geoError);
    //en lugar de marker1 , marker2 , marker 4 usamos destinations en current_order.html
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
    //lo siguiente se comentaria dado que los dealers hacen los calculos de tiempo
    var service = new google.maps.DistanceMatrixService();
    service.getDistanceMatrix(
        {
            // origins: [{lat: rest_lat, lng: rest_long}],
            origins: [{lat: 4.5981, lng: -74.0760}],
            //destinations: destinations,
            destinations: [{lat: 4.5981, lng: -75.0760}, {lat: 4.4521, lng: -74.0760}, {lat: 5.5981, lng: -69.0760}],
            //travelMode: 'BIKING',
            travelMode: 'DRIVING',
            avoidHighways: false,
            avoidTolls: false,
        }, callbackMatrix);
}
//en lugar de esto seria una funcion que ordene los dealers que van llegando
var callbackMatrix = function (response, status) {
    console.log(response)
    let min = response.rows[0].elements[0].duration.value,
        minIndex = 0;
    //usar minheap
    /*
    var heap = new Heap([2, 8, 5]);
    heap.push(6)
    heap.pop();
     8
    heap.peek();
     */
    for (let i = 1; i < response.rows[0].elements.length; i++) {
        if (min > response.rows[0].elements[i].duration.value) {
            min = response.rows[0].elements[i].duration.value;
            minIndex = i;
        }
    }
    console.log(response.destinationAddresses[minIndex]);
    calculateAndDisplayRoute({
        //lat: user_lat,
        // lng: user_long
        lat: 4.5981,
        lng: -74.0760
    }, response.destinationAddresses[minIndex]);
};

//muestra la posicion actual del dealer
//falta enviar esa posicion a la orden
let geoSuccess = function (position) {
    startPos = position;
    console.log(position)
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

