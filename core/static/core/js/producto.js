
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




