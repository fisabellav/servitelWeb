
const cantidadValor = document.getElementById('cantidad-valor');
const menosCantidad = document.getElementById('menos-cantidad');
const masCantidad = document.getElementById('mas-cantidad');

let cantidad = parseInt(cantidadValor.textContent);

menosCantidad.addEventListener('click', () => {
    if (cantidad > 1) {
        cantidad--;
        cantidadValor.textContent = cantidad;
    }
});

masCantidad.addEventListener('click', () => {
    cantidad++;
    cantidadValor.textContent = cantidad;
});



const phoneInput = document.querySelector('#idFono');
const iti = window.intlTelInput(phoneInput, {
    utilsScript: 'https://cdnjs.cloudflare.com/ajax/libs/intl-tel-input/17.0.8/js/utils.js',
    initialCountry: 'cl'
});

phoneInput.addEventListener('input', (e) => {
    const value = e.target.value.replace(/\D+/g, '');
    let formattedValue = '';

    // Verifica si el código de país seleccionado es Chile
    if (iti.getSelectedCountryData().iso2 === 'cl') {
        // Aplica el formato de número de teléfono específico para Chile
        if (value.startsWith('9')) {
            formattedValue = formatTelefono9(value);
        } else if (value.startsWith('2')) {
            formattedValue = formatTelefono2(value);
        } else {
            formattedValue = formatTelefono9(value);
        }

        // Limita a 9 dígitos solo para Chile
        if (value.length >= 9) {
            formattedValue = formattedValue.substring(0, 11);

        }


    } else {
        // Aplica el formato de número de teléfono por defecto
        iti.setNumber(value);
        formattedValue = iti.getNumber();

        if (value.length >= 12) {
            formattedValue = formattedValue.substring(0, 17);
        }
    }
    e.target.value = formattedValue;
});

function formatTelefono9(value) {
    if (value.length <= 1) {
        return value;
    } else if (value.length <= 5) {
        return value.replace(/(\d{1})(\d{1,4})/, '$1 $2');
    } else {
        return value.replace(/(\d{1})(\d{4})(\d{1,4})/, '$1 $2 $3');
    }
}

function formatTelefono2(value) {
    if (value.length <= 1) {
        return value;
    } else if (value.length <= 4) {
        return value.replace(/(\d{1})(\d{1,3})/, '$1 $2');
    } else if (value.length <= 7) {
        return value.replace(/(\d{1})(\d{4})(\d{1,2})/, '$1 $2 $3');
    } else {
        return value.replace(/(\d{1})(\d{2})(\d{3})(\d{1,2})/, '$1 $2-$3-$4');
    }
}
