// Cargar el carrito desde el almacenamiento local al cargar la página


let listProductHTML = document.querySelector('.all-products');
let body = document.querySelector('body');
let cart = [];



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

        addToCart(productData);
    }
});

const addToCart = (productData) => {
    let positionThisProductInCart = cart.findIndex((value) => value.id == productData.id);
    if (cart.length <= 0) {
        cart = [{
            id: productData.id,
            name: productData.name,
            image: productData.image,
            quantity: 1,
        }];
    } else if (positionThisProductInCart < 0) {
        cart.push({
            id: productData.id,
            name: productData.name,
            image: productData.image,
            quantity: 1,
        });
    } else {
        cart[positionThisProductInCart].quantity = cart[positionThisProductInCart].quantity + 1;
    }
    addCartToHTML();
    saveCartToLocalStorage(); // Guardar el carrito en el almacenamiento local después de actualizarlo
}

