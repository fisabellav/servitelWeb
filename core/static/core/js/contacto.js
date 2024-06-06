// Función para cargar el carrito desde el almacenamiento local
window.addEventListener('DOMContentLoaded', () => {
    console.log('DOMContentLoaded event fired');
    loadCartFromLocalStorage();
});

const loadCartFromLocalStorage = () => {
    const storedCart = localStorage.getItem('cart');
    if (storedCart) {
        cart = JSON.parse(storedCart);
        addCartToHTML(); // Agregar la lista de deseos al HTML
    }
};

// Función para agregar la lista de deseos al HTML
const addCartToHTML = () => {
    // Obtener el contenedor donde se mostrarán los productos de la lista de deseos
    const wishlistContainer = document.getElementById('wishlist-products');

    // Limpiar el contenido anterior en caso de que haya
    wishlistContainer.innerHTML = '';

    // Verificar si hay productos en la lista de deseos
    if (cart.length > 0) {
        // Iterar sobre los productos en la lista de deseos y agregarlos al contenedor HTML
        cart.forEach(product => {
            // Crear un elemento <li> para cada producto en la lista de deseos
            let listItem = document.createElement('div');
            listItem.classList.add('item');
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
        });
        
    } else {
        // Si no hay productos en la lista de deseos, mostrar un mensaje indicando que está vacía
        wishlistContainer.textContent = 'No hay productos en la lista de deseos.';
    }
};