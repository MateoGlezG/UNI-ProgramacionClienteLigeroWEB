
function send_ajax(id) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
        document.getElementById("pie").innerHTML = this.responseText;
        }
    };
    xhttp.open("GET", id, true);
    xhttp.send();
}

function enviar(event) {
    event.preventDefault(); // Evita el envío tradicional del formulario
    let form = document.getElementById("formulario-gestion");
    let queryString = new URLSearchParams(new FormData(form)).toString(); // Convierte los datos en una cadena GET

    send_ajax(form.action + "?" + queryString); // Llama a send_form con la URL y los parámetros del formulario

}


