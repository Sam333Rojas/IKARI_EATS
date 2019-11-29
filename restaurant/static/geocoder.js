//se ejecuta despues del primer login si el restaurante no tiene lat log
//convertir texto a lat y log para posteriormente enviarlo por post a la bd
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$(function () {
    var geocoder = new google.maps.Geocoder();
    var geocoder_OK = google.maps.GeocoderStatus.OK;
    if (address) {
        var res_lat;
        var res_log;

        geocoder.geocode({'address': address}, function (results, status) {
            if (status === geocoder_OK) {
                res_lat = results[0].geometry.location.lat();
                res_log = results[0].geometry.location.lng();
                console.log(res_lat, res_log);
                $.post({
                    data: {'lat': res_lat, 'log': res_log},
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
            }
        });
    }
});
