// Selecciona todos los elementos con la clase 'modal-borrar'
// Selecciona todos los elementos con la clase 'modal-borrar'
const modalBorrarElements = document.querySelectorAll('.modal-borrar');

// Añade un evento de clic a cada uno de esos elementos
modalBorrarElements.forEach(function (element) {
    element.addEventListener('click', function (event) {
        event.preventDefault();
        const href = this.getAttribute('data-href');

        Swal.fire({
            title: "¿Estás seguro?",
            text: "¡No podrás revertir esto!",
            icon: "warning",
            showCancelButton: true,
            confirmButtonColor: "#d33",
            cancelButtonColor: "#3085d6",
            confirmButtonText: "Sí, ¡elimínalo!"
            
            
            
        }).then((result) => {
            if (result.isConfirmed) {
                window.location.href = href;
            }
        });
    });
});