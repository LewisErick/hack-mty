/**
 * Created by lagwy on 27/08/16.
 */
var descripciones = document.getElementsByClassName("lib-desc");
for (var i = 0; i < descripciones.length; i++){
    var desc = descripciones[i].innerHTML;
    var newDesc;
    if (desc.length >= 100){
        newDesc = desc.substr(0,96) + "...";
        descripciones[i].innerHTML = newDesc;
    } else {

    }
}