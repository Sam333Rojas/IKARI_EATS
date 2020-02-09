//cposicion  del cliente

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
console.log("1");
$(function () {
    var client_lat;
    var client_log;

    console.log("2");

    var geoSuccess = function (position) {
        console.log("3");
        startPos = position;
        console.log(position);
        client_lat = position.coords.latitude;
        client_lat = position.coords.longitude;
        console.log("4");
        console.log(client_lat, client_log);
        $.post({
            data: {'lat': client_lat, 'log': client_log},
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
});
