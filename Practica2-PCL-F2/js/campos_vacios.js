function validar(event) {
    if (event) event.preventDefault(); 

    let form = document.getElementById("formulario-gestion");
    
    // 1. Extraer valores de texto y select
    let empleado = form.elements["empleado"].value.trim();
    let departamento = form.elements["departamento"].value; // Será "" si no elige uno
    let planta = form.elements["planta"].value;             // Será "" si no elige uno
    
    // 2. Comprobar si hay algún radio button marcado
    // querySelector busca el input con nombre 'tipo' que esté :checked
    let tipoPuesto = form.querySelector('input[name="tipo"]:checked');

    let faltanCampos = [];

    // 3. Lógica de validación
    if (empleado === "") {
        faltanCampos.push("- Nombre del Empleado");
    }
    if (departamento === "") {
        faltanCampos.push("- Departamento (No seleccionado)");
    }
    if (!tipoPuesto) {
        faltanCampos.push("- Tipo de espacio (Radio button)");
    }
    if (planta === "") {
        faltanCampos.push("- Planta (No seleccionada)");
    }

    // 4. Lógica de confirmación o envío
    if (faltanCampos.length > 0) {
        let mensaje = "Atención: Los siguientes campos están vacíos:\n\n" + 
                      faltanCampos.join("\n") +
                      "\n\n¿Desea enviar la reserva de todos modos?";
        
        if (!confirm(mensaje)) {
            return false; // El usuario pulsa 'Cancelar' y se queda en el formulario
        }
    }

    // 5. Si llega aquí es que todo está OK o el usuario aceptó el confirm
    enviar(event); 
}
