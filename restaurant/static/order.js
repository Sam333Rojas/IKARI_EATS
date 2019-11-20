//Restaurant
/*
se conecta con active_sales.html
recibe los candidatos a dealer
los ordena en un min heap tama;o 20 durante 5 minutos
si no hay candidatos aumenta el tiempo maximo y reenvia la solicitud
para aumentar el tiempo se propone la funcion (3x/(x+5)) que tiende a 3 siendo el numero de horas,inicialmente vale 0,5
en caso de que el dealer cancele asigna al siguiente en el heap
se cambia la order con el dealer seleccionado y se envia a client y a dealer
 */
