function cambiarCapas(id) {
    document.getElementById("datos_empleado").style.display = "none";
    document.getElementById("reserva_puesto").style.display = "none";
    document.getElementById("equipamiento").style.display = "none";
    document.getElementById("notas_adicionales").style.display = "none";
    document.getElementById(id).style.display = "block";
    }