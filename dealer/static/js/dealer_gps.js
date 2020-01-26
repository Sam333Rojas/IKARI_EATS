//calcular posicion actual del dealer y enviarla por post

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$(function () {
    var dealer_lat;
    var dealer_log;
    var geoSuccess = function (position) {
        startPos = position;
        console.log(position);
        dealer_lat = position.coords.latitude;
        dealer_lat = position.coords.longitude;
        $.post({
            data: {'lat': dealer_lat, 'log': dealer_log},
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
    var geoError = function (error) {
        switch (error.code) {
            case error.TIMEOUT:
                console.log('error');
                break;
        }
    };
    navigator.geolocation.getCurrentPosition(geoSuccess, geoError);
    console.log(dealer_lat, dealer_log);
});
