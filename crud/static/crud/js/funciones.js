document.addEventListener('DOMContentLoaded', function () {
    // Selecciona todos los elementos que tienen la clase 'product-price'
    const priceElements = document.querySelectorAll('.product-price');

    // Itera sobre cada elemento y aplica el formato
    priceElements.forEach(function (element) {
        // Obtén el precio del atributo data-price y conviértelo en número
        const price = parseFloat(element.getAttribute('data-price'));

        // Formatea el precio usando Intl.NumberFormat
        const formattedPrice = new Intl.NumberFormat('es-CL', {
            style: 'currency',
            currency: 'CLP',
            minimumFractionDigits: 0
        }).format(price);

        // Actualiza el contenido del elemento con el precio formateado
        element.textContent = formattedPrice;
    });
});

document.addEventListener('DOMContentLoaded', function () {
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

    const statusSelect = document.getElementById('status');
    const statusForm = document.getElementById('status-form');

    if(statusSelect){
        statusSelect.addEventListener('change', function () {
            statusForm.submit();
        });
    }

    // Manejar clic en el botón de confirmación
    document.querySelectorAll('.btn-confirm').forEach(function (button) {
        button.addEventListener('click', function () {
            var orderId = this.getAttribute('data-order-id');
            updateOrderStatus(orderId, 'CF');
        });
    });

    // Manejar clic en el botón de cancelación
    document.querySelectorAll('.btn-cancel').forEach(function (button) {
        button.addEventListener('click', function () {
            var orderId = this.getAttribute('data-order-id');
            Swal.fire({
                title: "¿Estás seguro?",
                text: "¡No podrás revertir esto!",
                icon: "warning",
                showCancelButton: true,
                confirmButtonColor: "#d33",
                cancelButtonColor: "#3085d6",
                confirmButtonText: "Sí, ¡cancélalo!"
            }).then((result) => {
                if (result.isConfirmed) {
                    updateOrderStatus(orderId, 'CN');
                }
            });
        });
    });

    function updateOrderStatus(orderId, status) {
        // Validar que el estado enviado esté entre las opciones válidas
        const validStatuses = ['PC', 'CF', 'EP', 'EN', 'CN'];
        if (!validStatuses.includes(status)) {
            alert('Estado no válido.');
            return;
        }

        fetch(`/order/update-status/${orderId}/${status}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
                'Content-Type': 'application/json'
            },
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    const orderRow = document.querySelector(`tr[data-order-id="${orderId}"]`);
                    const statusCell = orderRow.querySelector('.order-status');
                    statusCell.querySelector('a').textContent = getStatusText(status); // Actualizar el enlace del estado

                    function getStatusText(status) {
                        switch (status) {
                            case 'PC':
                                return 'Pendiente Confirmación';
                            case 'CF':
                                return 'Confirmado';
                            case 'EP':
                                return 'En preparación';
                            case 'EN':
                                return 'Entregado';
                            case 'CN':
                                return 'Cancelado';
                            default:
                                return '';
                        }
                    }
                            
                } else {
                    alert('Error al actualizar el estado del pedido: ' + (data.error || 'Desconocido'));
                }
            })
            .catch(error => {
                alert('Error en la solicitud AJAX: ' + error.message);
            });
    }
});

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
