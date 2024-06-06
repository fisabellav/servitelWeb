const form = document.querySelector('.custom-validation');
// Ocultar el error de longitud mínima al cargar la página
document.getElementById("error_nombre_min").style.display = "none";
document.getElementById("error_nombre_max").style.display = "none";
document.getElementById("error_apellido_min").style.display = "none";
document.getElementById("error_apellido_max").style.display = "none";
document.getElementById("error_fono").style.display = "none";
document.getElementById("error_nacimiento").style.display = "none";
document.getElementById("error_fecha").style.display = "none";
document.getElementById("error_comuna").style.display = "none";
document.getElementById("error_checkbox").style.display = "none";



// Agregar un listener de eventos al elemento con id "idNombre"
// para que se ejecute la función "validarNombre" cuando el elemento pierda el foco
document.getElementById("idNombre").addEventListener("blur", function () {
    let nombre = document.getElementById("idNombre").value;
    // Llamar a la función "validarNombre" con el valor del nombre como argumento
    validarNombre(nombre);
});
document.getElementById("idApellido").addEventListener("blur", function () {
    let apellido = document.getElementById("idApellido").value;
    // Llamar a la función "validarNombre" con el valor del nombre como argumento
    validarApellido(apellido);
});
document.getElementById("idFono").addEventListener("blur", function () {
    let fono = document.getElementById("idFono").value;
    // Llamar a la función "validarNombre" con el valor del nombre como argumento
    validarFono(fono);

    const prefijoInput = document.querySelector('#prefijo-hidden');
    const prefijoSelect = document.querySelector('.iti');
    const prefijoElement = prefijoSelect.querySelector('[aria-selected="true"]');

    let prefijo = '+'; // Variable para almacenar el prefijo seleccionado

    if (prefijoElement) {
        prefijo += prefijoElement.getAttribute('data-dial-code'); // Obtiene el valor de data-dial-code
    }

    prefijoInput.value = prefijo;
});
document.getElementById("comuna-select").addEventListener("blur", function () {
    let comuna = document.getElementById("comuna-select").value;
    // Llamar a la función "validarNombre" con el valor del nombre como argumento
    validarComuna(comuna);
});
document.getElementById("idFecha_nac").addEventListener("blur", function () {
    // Obtener el campo de fecha de nacimiento
    let fecha_nac = document.getElementById("idFecha_nac").value;
    // Llamar a la función "validarNombre" con el valor del nombre como argumento
    validarFechaNac(fecha_nac);
});

form.addEventListener('submit', (e) => {
    let isValid = false; // Inicialmente asumimos que el formulario no es válido

    if (validarNombre(document.getElementById("idNombre").value) &&
        validarApellido(document.getElementById("idApellido").value) &&
        validarFono(document.getElementById("idFono").value) &&
        validarFechaNac(document.getElementById("idFecha_nac").value) &&
        validarComuna(document.getElementById("comuna-select").value) &&
        document.getElementById("gridCheck").checked) {
        
        // Si todas las validaciones son exitosas y el checkbox está marcado, el formulario es válido
        isValid = true;
    } else {
        // Si hay algún error de validación o el checkbox no está marcado, el formulario no es válido
        document.getElementById("error_checkbox").style.display = "inline";
    }

    // Previene el envío del formulario si no es válido
    if (!isValid) {
        e.preventDefault();
    }
});

// Definir la función "validarNombre"
function validarNombre(nombre) {
    if (nombre.trim().length < 3) {
        // Mostrar el error de longitud mínima si el nombre es demasiado corto
        document.getElementById("error_nombre_max").style.display = "none";
        document.getElementById("error_nombre_min").style.display = "inline";
        // Agregar la clase "is-invalid" al elemento con id "idNombre"
        document.getElementById("idNombre").classList.add("is-invalid");
        // Devolver falso para indicar que el nombre no es válido
        return false;
    } else if (nombre.trim().length > 20) {
        // Ocultar el error de longitud mínima y mostrar el error de longitud máxima
        // si el nombre es demasiado largo
        document.getElementById("error_nombre_min").style.display = "none";
        document.getElementById("error_nombre_max").style.display = "inline";
        // Agregar la clase "is-invalid" al elemento con id "idNombre"
        document.getElementById("idNombre").classList.add("is-invalid");
        // Devolver falso para indicar que el nombre no es válido
        return false;
    } else {
        // Ocultar los errores de longitud mínima y máxima
        document.getElementById("error_nombre_min").style.display = "none";
        document.getElementById("error_nombre_max").style.display = "none";
        // Quitar la clase "is-invalid" y agregar la clase "is-valid" al elemento con id "idNombre"
        document.getElementById("idNombre").classList.remove("is-invalid");
        document.getElementById("idNombre").classList.add("is-valid");
        // Devolver verdadero para indicar que el nombre es válido
        return true;
    }
}

function validarApellido(apellido) {
    if (apellido.trim().length < 3) {
        document.getElementById("error_apellido_min").style.display = "inline";
        document.getElementById("idApellido").classList.add("is-invalid");
        return false;
    } else if (apellido.trim().length > 20) {
        document.getElementById("error_apellido_min").style.display = "none";
        document.getElementById("error_apellido_max").style.display = "inline";
        document.getElementById("idApellido").classList.add("is-invalid");
        return false;
    } else {
        document.getElementById("error_apellido_min").style.display = "none";
        document.getElementById("error_apellido_max").style.display = "none";
        document.getElementById("idApellido").classList.remove("is-invalid");
        document.getElementById("idApellido").classList.add("is-valid");
        return true;
    }
}

function validarFono(fono) {
    if (fono.trim().length < 3) {
        document.getElementById("error_fono").style.display = "inline";
        document.getElementById("idFono").classList.add("is-invalid");
        return false;
    } else {
        document.getElementById("error_fono").style.display = "none";
        document.getElementById("error_fono").style.display = "none";
        document.getElementById("idFono").classList.remove("is-invalid");
        document.getElementById("idFono").classList.add("is-valid");
        return true;
    }
}

function validarFechaNac(fecha_nac) {
    if (fecha_nac === "") {
        document.getElementById("error_nacimiento").style.display = "inline";
        document.getElementById("error_fecha").style.display = "none";
        document.getElementById("idFecha_nac").classList.add("is-invalid");
        return false;
    } else{
        // Convertir la fecha de nacimiento a un objeto Date
        var fechaNacimiento = new Date(fecha_nac);
        
        // Calcular la fecha actual
        var fechaActual = new Date();
        
        // Calcular la edad restando la fecha actual menos la fecha de nacimiento
        var edad = fechaActual.getFullYear() - fechaNacimiento.getFullYear();
        
        // Restar un año si el día actual es antes del día de nacimiento
        if (fechaNacimiento.getMonth() > fechaActual.getMonth() || 
            (fechaNacimiento.getMonth() === fechaActual.getMonth() && fechaNacimiento.getDate() > fechaActual.getDate())) {
            edad--;
        }
        
        // Verificar si la edad está dentro del rango deseado (entre 18 y 120 años)
        if (edad >= 18 && edad <= 120) {
            // La fecha de nacimiento es válida
            document.getElementById("error_nacimiento").style.display = "none";
            document.getElementById("error_fecha").style.display = "none";
            document.getElementById("idFecha_nac").classList.remove("is-invalid");
            document.getElementById("idFecha_nac").classList.add("is-valid");
            return true;
        } else {
            // La fecha de nacimiento no está dentro del rango deseado
            document.getElementById("error_fecha").style.display = "inline";
            document.getElementById("error_nacimiento").style.display = "none";
            document.getElementById("idFecha_nac").classList.add("is-invalid");
            return false;
        }
    }
}

function validarComuna(comuna) {
    if (comuna == "") {
        document.getElementById("error_comuna").style.display = "inline";
        document.getElementById("comuna-select").classList.add("is-invalid");
        return false;
    } else {
        document.getElementById("error_comuna").style.display = "none";
        document.getElementById("comuna-select").classList.remove("is-invalid");
        document.getElementById("comuna-select").classList.add("is-valid");
        return true;
    }
}