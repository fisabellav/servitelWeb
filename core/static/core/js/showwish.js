let iconCart = document.querySelector('.icon-cart');
let iconCartSpan = document.querySelector('.icon-cart span');

let listCartHTML = document.querySelector('.listCart');
let closeCart = document.querySelector('.close');
let solicitarForm = document.querySelector('.solicitar');

iconCart.addEventListener('click', () => {
    const cartTab = document.querySelector('.cartTab');
    cartTab.classList.toggle('showCart');
    document.body.classList.toggle('showCart');
});

closeCart.addEventListener('click', () => {
    const cartTab = document.querySelector('.cartTab');
    cartTab.classList.toggle('showCart');
    document.body.classList.toggle('showCart');
});



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


const addCartToHTML = () => {
    listCartHTML.innerHTML = '';
    let totalQuantity = 0;
    if (cart.length > 0) {
        cart.forEach(item => {
            totalQuantity = totalQuantity + item.quantity;
            let newItem = document.createElement('div');
            newItem.classList.add('item');
            newItem.dataset.id = item.id;

            newItem.innerHTML = `
        <div class="image">
            <img src="${item.image}">
        </div>
        <div class="name">
            ${item.name}
        </div>
        
        <div class="quantity">
            <span class="minus"><</span>
            <span>${item.quantity}</span>
            <span class="plus">></span>
        </div>
        <div class="remove">
            <i class="fa fa-trash"></i>
        </div>
        `;
            listCartHTML.appendChild(newItem);
        })
    }
    iconCartSpan.innerText = totalQuantity;
}

// Función para eliminar producto del carrito
const removeFromCart = (product_id) => {
    cart = cart.filter(item => item.id !== product_id);
    addCartToHTML();
    saveCartToLocalStorage(); // Guardar carrito en localStorage
}

// Función para guardar el carrito en el almacenamiento local
const saveCartToLocalStorage = () => {
    localStorage.setItem('cart', JSON.stringify(cart));
}

// Función para cargar el carrito desde el almacenamiento local
const loadCartFromLocalStorage = () => {
    const storedCart = localStorage.getItem('cart');
    if (storedCart) {
        cart = JSON.parse(storedCart);
        addCartToHTML(); // Actualizar la interfaz de usuario con el contenido del carrito cargado
    }
};

// Evento para cargar el carrito desde el almacenamiento local cuando se carga la página
window.addEventListener('DOMContentLoaded', () => {
    loadCartFromLocalStorage();
});