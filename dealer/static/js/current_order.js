var map;
var time;
function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: dealer_lat, lng: dealer_log},
        zoom: 10
    });
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
            destinations: [{lat: res_lat, lng: res_log}],
            travelMode: 'BICYCLING',
            avoidHighways: false,
            avoidTolls: false,
        }, callbackMatrix);
}
var callbackMatrix = function (response, status) {
    var min = response.rows[0].elements[0].duration.value, minIndex = 0;c

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

