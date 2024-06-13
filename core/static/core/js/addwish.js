// Cargar el carrito desde el almacenamiento local al cargar la página

import {addToCart } from './carrito.js';
let listProductHTML = document.querySelector('.all-products');



listProductHTML.addEventListener('click', (event) => {
    let positionClick = event.target;
    if (positionClick.classList.contains('deseos')) {
        let productElement = positionClick.closest('.product');
        let productId = productElement.dataset.id;
        let productName = productElement.querySelector('.product-title').textContent;
        
        let productImage = productElement.querySelector('img').src;

        let productData = {
            id: productId,
            name: productName,
            image: productImage,
        };
        console.log(productId)
        addToCart(productData);
    }
});



