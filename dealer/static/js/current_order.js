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
        center: {lat: dealer_lat, lng: dealer_log},
        zoom: 10
    });
    navigator.geolocation.getCurrentPosition(geoSuccess, geoError);
    var restaurant_marker = new google.maps.Marker({
        position: {lat: res_lat, lng: res_log},
        map: map,
        title: 'Restaurante'
    });
    var dealer_marker = new google.maps.Marker({
        position: {lat: dealer_lat, lng: -dealer_log},
        map: map,
        title: 'Deliverer'
    });

    var service = new google.maps.DistanceMatrixService();
    service.getDistanceMatrix(
        {
            origins: [{lat: dealer_lat, lng: dealer_log}],
            // origins: [{lat: 4.5981, lng: -74.0760}],
            destinations: [{lat: res_lat, lng: res_log}],
            // destinations: [{lat: 4.5981, lng: -75.0760}, {lat: 4.4521, lng: -74.0760}, {lat: 5.5981, lng: -69.0760}],
            travelMode: 'BIKING',
            avoidHighways: false,
            avoidTolls: false,
        }, callbackMatrix);
}
var callbackMatrix = function (response, status) {
    var min = response.rows[0].elements[0].duration.value, minIndex = 0;

    for (var i = 1; i < response.rows[0].elements.length; i++) {
        if (min > response.rows[0].elements[i].duration.value) {
            min = response.rows[0].elements[i].duration.value;
            minIndex = i;
        }
    }

    time = response.rows[0].elements[minIndex].duration.value;
    $("#time").html("El tiempo estimado es de " + time);
    $("#cancel-solicitude").removeAttribute("hidden");
    calculateAndDisplayRoute({
        lat: dealer_lat,
        lng: dealer_log
    }, response.destinationAddresses[minIndex]);

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
};

function csrfSafeMethod(method) {
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

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

