//se ejecuta despues del primer login si el restaurante no tiene lat log
//convertir texto a lat y log para posteriormente enviarlo por post a la bd

/*var geocoder = new google.maps.Geocoder();
var res_lat;
var res_log;
geocoder.geocode( { 'address': address}, function(results, status) {
  if (status == google.maps.GeocoderStatus.OK) {
    res_lat = results[0].geometry.location.lat();
    res_log = results[0].geometry.location.lng();
  }
});


// emviar por post a BD
var http = new XMLHttpRequest();
var url = 'get_data.php';
var params = 'orem=ipsum&name=binny';
http.open('POST', url, true);

//Send the proper header information along with the request
http.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');

http.onreadystatechange = function() {//Call a function when the state changes.
    if(http.readyState == 4 && http.status == 200) {
        alert(http.responseText);
    }
}
http.send(params);

 */