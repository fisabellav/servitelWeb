import {addToCart } from './carrito.js';
let listProductHTML = document.querySelector('.product-detail');
document.addEventListener('DOMContentLoaded', function() {

    let cantidadValorInput = document.getElementById('cantidad-valor');
    let cantidadValorLabel = document.getElementById('cantidad-valor-label');
    let menosCantidad = document.getElementById('menos-cantidad');
    let masCantidad = document.getElementById('mas-cantidad');
    let idCantidadInput = document.getElementById('idCantidad');

    
    let cantidad = parseInt(cantidadValorInput.value);

    function actualizarCantidad() {
        cantidadValorInput.value = cantidad;
        cantidadValorLabel.textContent = cantidad;
        if(idCantidadInput){
            idCantidadInput.value = cantidad
        }
        
    }

    menosCantidad.addEventListener('click', () => {
        if (cantidad > 1) {
            cantidad--;
            actualizarCantidad();
        }
    });

    masCantidad.addEventListener('click', () => {
        cantidad++;
        actualizarCantidad();
    });

    cantidadValorInput.addEventListener('input', () => {
        cantidad = parseInt(cantidadValorInput.value);
        actualizarCantidad();
    });

    if(idCantidadInput){
        idCantidadInput.addEventListener('input', () => {
            cantidad = parseInt(idCantidadInput.value);
            actualizarCantidad();
        });
    }

    actualizarCantidad();

    const modalBtn = document.getElementById('orderBtn');

    if(modalBtn){
        modalBtn.addEventListener('click', function () {
            Swal.fire({
                title: "¿Estás seguro?",
                text: "¿Quieres enviar la solicitud?",
                icon: "question",
                showCancelButton: true,
                confirmButtonColor: "#3085d6",
                cancelButtonColor: "#d33",
                confirmButtonText: "Sí, enviar solicitud",
                cancelButtonText: "Cancelar"
            }).then((result) => {
                if (result.isConfirmed) {
                    // Enviar el formulario
                    document.getElementById('order-form').submit();
                }
            }).catch(error => {
                console.error('Error:', error);
                Swal.fire({
                    title: 'Error',
                    text: 'Hubo un problema al enviar tu pedido. Por favor, intenta nuevamente.',
                    icon: 'error',
                    confirmButtonText: 'OK'
                });
            });
        });
    }

    

    document.querySelector('.add-to-wishlist').addEventListener('click', function () {
        let heart = this;
        let heartRect = heart.getBoundingClientRect();

        // Crear y clonar el corazón
        let heartClone = heart.cloneNode(true);
        heartClone.style.position = 'absolute';
        heartClone.style.left = `${heartRect.left}px`;
        heartClone.style.top = `${heartRect.top}px`;
        heartClone.style.width = `${heartRect.width}px`;
        heartClone.style.height = `${heartRect.height}px`;
        heartClone.style.zIndex = '1000';
        heartClone.style.transition = 'transform 1s, opacity 1s';
        document.body.appendChild(heartClone);

        // Obtener la posición del corazón en el navbar
        let navbarHeart;
            if (window.matchMedia("(max-width: 768px)").matches) {
                // Modo móvil
                navbarHeart = document.querySelector('.dropdown_menu .icon-cart');
            } else {
                // Modo escritorio
                navbarHeart = document.querySelector('.icon-navbar');
            }

        let navbarRect = navbarHeart.getBoundingClientRect();

        // Calcular el desplazamiento
        let translateX = navbarRect.left + (navbarRect.width / 2) - heartRect.left - (heartRect.width / 2);
        let translateY = navbarRect.top + (navbarRect.height / 2) - heartRect.top - (heartRect.height / 2);

        // Aplicar estilos para la animación
        requestAnimationFrame(() => {
            heartClone.style.transform = `translate(${translateX}px, ${translateY}px)`;
            heartClone.style.opacity = '0';
        });

        heartClone.addEventListener('transitionend', function () {
            heartClone.remove();
            // Actualizar el contador
        });
    });
});




listProductHTML.addEventListener('click', (event) => {
    let positionClick = event.target;
    if (positionClick.classList.contains('deseos')) {
        let productElement = positionClick.closest('.product');
        let cantidadValor = document.getElementById('cantidad-valor-label');

        if (cantidadValor) {
            let productId = productElement.dataset.id;
            let productName = productElement.querySelector('.product-title').textContent;
            let productQuantity = parseInt(cantidadValor.textContent);
            let productImage = productElement.querySelector('img').src;

            let productData = {
                id: productId,
                name: productName,
                image: productImage,
                quantity: productQuantity,
            };
            addToCart(productData);
            
        } else {
            console.error('Cantidad valor no encontrado en el producto:', productElement);
        }
    }
});