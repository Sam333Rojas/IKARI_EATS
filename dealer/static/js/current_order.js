//Dealer
/*
calcula la ruta entre el y el restaurante
envia el tiempo correspondiente
si es aceptaddo traza la ruta entre el y el restaurante
si es aceptado cambia su estatus y lo envia por post
 */

var map;
var time;
function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
        //lo centramos en el dealer siendo
        // center: {lat: dealer_lat, lng: dealer_log},
        center: {lat: 4.7110, lng: -74.0721},
        zoom: 10
    });
    navigator.geolocation.getCurrentPosition(geoSuccess, geoError);
    //
    /*
    var restaurant_marker = new google.maps.Marker({
        position: {lat: res_lat, lng: res_log},
        map: map,
        title: 'Hello World!'
    });
    var dealer_marker = new google.maps.Marker({
        position: {lat: dealer_lat, lng: -dealer_log},
        map: map,
        title: 'Hello World!'
    });
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
            // origins: [{lat: dealer_lat, lng: dealer_log}],
            origins: [{lat: 4.5981, lng: -74.0760}],
            //destinations: [{lat: res_lat, lng: res_log}],
            destinations: [{lat: 4.5981, lng: -75.0760}, {lat: 4.4521, lng: -74.0760}, {lat: 5.5981, lng: -69.0760}],
            //travelMode: 'BIKING',
            travelMode: 'DRIVING',
            avoidHighways: false,
            avoidTolls: false,
        }, callbackMatrix);
}
var callbackMatrix = function (response, status) {
    console.log(response)
    var min = response.rows[0].elements[0].duration.value,
        minIndex = 0;

    for (var i = 1; i < response.rows[0].elements.length; i++) {
        if (min > response.rows[0].elements[i].duration.value) {
            min = response.rows[0].elements[i].duration.value;
            minIndex = i;
        }
    }
    console.log(response.destinationAddresses[minIndex]);
    //guardamos el tiempo en la variable time para enviarlo a BD
    //time = response.rows[0].elements[minIndex].duration.value;
    //no es necesario trazar ruta en el proceso
    calculateAndDisplayRoute({
        //lat: user_lat,
        // lng: user_long
        lat: 4.5981,
        lng: -74.0760
    }, response.destinationAddresses[minIndex]);
};

//ENVIAR TIEMPO A BD SOLICITUDE
/*
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$(function () {
    console.log(time);
    $.post({
        data: {'time': time},
        url: '',
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        },
        success: function () {
            console.log('bien!');
        }
    });


});
//
 */
function calculateAndDisplayRoute(pointA, pointB) {
    var directionsService = new google.maps.DirectionsService;
    var directionsRenderer = new google.maps.DirectionsRenderer;
    directionsRenderer.setMap(map);
    directionsService.route({
            origin: pointA,
            destination: pointB,
            //travelMode:
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

