// Función para cargar el carrito desde el almacenamiento local
import { removeFromCart } from './carrito.js';

let listCartHTML = document.querySelector('.listCart');
let iconCartSpan = document.querySelector('.icon-cart span');
let cart = [];

listCartHTML.addEventListener('click', (event) => {
    let positionClick = event.target;
    if (positionClick.classList.contains('minus') || positionClick.classList.contains('plus')) {
        let product_id = positionClick.parentElement.parentElement.dataset.id;
        let type = 'minus';
        if (positionClick.classList.contains('plus')) {
            type = 'plus';
        }
        changeQuantityCart(product_id, type);
    }
    if (positionClick.classList.contains('fa-trash')) {
        let product_id = positionClick.closest('.item').dataset.id;
        removeFromCart(product_id);
    }
})

const changeQuantityCart = (product_id, type) => {
    let positionItemInCart = cart.findIndex((value) => value.id == product_id);
    if (positionItemInCart >= 0) {
        let info = cart[positionItemInCart];
        switch (type) {
            case 'plus':
                cart[positionItemInCart].quantity = cart[positionItemInCart].quantity + 1;
                break;

            case 'minus':
                if (cart[positionItemInCart].quantity > 1) {
                    cart[positionItemInCart].quantity = cart[positionItemInCart].quantity - 1;
                }
                break;
        }
        addCartToHTML();
        saveCartToLocalStorage(); // Guardar el carrito en el almacenamiento local después de actualizarlo
    }
}

window.addEventListener('DOMContentLoaded', () => {
    loadCartFromLocalStorage();
});

const loadCartFromLocalStorage = () => {
    const storedCart = localStorage.getItem('cart');
    if (storedCart) {
        cart = JSON.parse(storedCart);
        addCartToHTML(); // Actualizar la interfaz de usuario con el contenido del carrito cargado

    }
};

const saveCartToLocalStorage = () => {
    localStorage.setItem('cart', JSON.stringify(cart));
}

// Función para agregar la lista de deseos al HTML
const addCartToHTML = () => {
    // Obtener el contenedor donde se mostrarán los productos de la lista de deseos
    const wishlistContainer = document.getElementById('wishlist-products');

    // Limpiar el contenido anterior en caso de que haya
    wishlistContainer.innerHTML = '';
    let totalQuantity = 0; 
    // Verificar si hay productos en la lista de deseos
    if (cart.length > 0) {
        // Iterar sobre los productos en la lista de deseos y agregarlos al contenedor HTML
        cart.forEach(product => {
            totalQuantity += product.quantity;
            // Crear un elemento <li> para cada producto en la lista de deseos
            let listItem = document.createElement('div');
            listItem.classList.add('item');
            listItem.classList.add('my-2');
            listItem.dataset.id = product.id;
            // Asignar el nombre del producto como contenido del elemento <li>
            listItem.innerHTML = `
            <div class="image">
            <img src="${product.image}">
            </div>
            <div class="name">
                ${product.name}
            </div>
            
            <div class="quantity">
                <span class="minus"><</span>
                <span>${product.quantity}</span>
                <span class="plus">></span>
            </div>
            <div class="remove">
                <i class="fa fa-trash"></i>
            </div>
            `;
            wishlistContainer.appendChild(listItem);

            let hr = document.createElement('hr');
            wishlistContainer.appendChild(hr);
        });
        
    } else {
        // Si no hay productos en la lista de deseos, mostrar un mensaje indicando que está vacía
        wishlistContainer.innerHTML = '<div class="text-center text-md-start m-md-3"> No hay productos en la lista de deseos.</div>';
    }   
    iconCartSpan.innerText = totalQuantity;
};

document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById('formulario');
    form.addEventListener('submit', function(event) {
        const wishlist = localStorage.getItem('cart');
        document.getElementById('wishlist').value = wishlist ? wishlist : '[]';
    });
});