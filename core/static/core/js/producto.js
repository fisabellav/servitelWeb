
document.addEventListener('DOMContentLoaded', function() {

    let cantidadValor = document.getElementById('cantidad-valor');
    let cantidadSeleccionada = document.getElementById('cantidad-seleccionada');
    let menosCantidad = document.getElementById('menos-cantidad');
    let masCantidad = document.getElementById('mas-cantidad');

    let cantidad = parseInt(cantidadValor.textContent);

    function actualizarCantidadSeleccionada() {
        cantidadSeleccionada.value = cantidad;
    }

    menosCantidad.addEventListener('click', () => {
        if (cantidad > 1) {
            cantidad--;
            cantidadValor.textContent = cantidad;
            actualizarCantidadSeleccionada();
        }
    });

    masCantidad.addEventListener('click', () => {
        cantidad++;
        cantidadValor.textContent = cantidad;
        actualizarCantidadSeleccionada();
    });

    actualizarCantidadSeleccionada();
});

