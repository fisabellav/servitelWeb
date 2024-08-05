import { loadCartFromLocalStorage} from './carrito.js';

document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('orderButton').addEventListener('click', function () {
        Swal.fire({
            title: "¿Estás seguro?",
            text: "¿Quieres enviar el carrito?",
            icon: "question",
            showCancelButton: true,
            confirmButtonColor: "#3085d6",
            cancelButtonColor: "#d33",
            confirmButtonText: "Sí, enviar carrito",
            cancelButtonText: "Cancelar"
        }).then((result) => {
            if (result.isConfirmed) {
                // Recopilar los productos en el carrito del localStorage
                const storedCart = localStorage.getItem('cart');
                if (storedCart) {
                    const cartItems = JSON.parse(storedCart);
                    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

                    // Enviar el carrito al servidor
                    fetch('/neworder/', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRFToken': csrfToken
                        },
                        body: JSON.stringify({ items: cartItems })
                    })
                        .then(response => response.json())
                        .then(data => {
                            if (data.success) {
                                Swal.fire({
                                    title: 'Pedido Confirmado',
                                    text: 'Pedido realizado. Pronto te llegará un mail de confirmación',
                                    icon: 'success',
                                    confirmButtonText: 'OK'
                                }).then(() => {
                                    // Limpia el localStorage y redirige a otra página si es necesario
                                    localStorage.removeItem('cart');
                                    loadCartFromLocalStorage();
                                    // window.location.href = "{% url 'product-list' %}";
                                });
                            } else {
                                // Error al enviar el carrito
                                Swal.fire({
                                    title: 'Error',
                                    text: 'Hubo un problema al enviar el carrito. Por favor, intenta nuevamente.',
                                    icon: 'error',
                                    confirmButtonText: 'OK'
                                });
                            }
                        })
                        .catch(error => {
                            console.error('Error:', error);
                            Swal.fire({
                                title: 'Error',
                                text: 'Hubo un problema al enviar el carrito. Por favor, intenta nuevamente.', error,
                                icon: 'error',
                                confirmButtonText: 'OK'
                            });
                        });

                }
            }
        })
            .catch(error => {
                console.error('Error:', error);
                Swal.fire({
                    title: 'Error',
                    text: error,
                    icon: 'error',
                    confirmButtonText: 'OK'
                });
            });
    });
});