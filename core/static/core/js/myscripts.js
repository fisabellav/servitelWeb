let listProductHTML = document.querySelector('.all-products');
let listCartHTML = document.querySelector('.listCart');
let iconCart = document.querySelector('.icon-cart');
let iconCartSpan = document.querySelector('.icon-cart span');
let body = document.querySelector('body');
let closeCart = document.querySelector('.close');
let cart = [];

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

listProductHTML.addEventListener('click', (event) => {
    let positionClick = event.target;
    if (positionClick.classList.contains('carrito')) {
        let productElement = positionClick.closest('.product');
        let productId = productElement.dataset.id;
        let productName = productElement.querySelector('.product-title').textContent;
        let productPrice = productElement.querySelector('.product-price').textContent;
        let productImage = productElement.querySelector('img').src;

        let productData = {
            id: productId,
            name: productName,
            price: productPrice,
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
            price: productData.price,
            image: productData.image,
            quantity: 1,
        }];
    } else if (positionThisProductInCart < 0) {
        cart.push({
            id: productData.id,
            name: productData.name,
            price: productData.price,
            image: productData.image,
            quantity: 1,
        });
    } else {
        cart[positionThisProductInCart].quantity = cart[positionThisProductInCart].quantity + 1;
    }
    addCartToHTML();
    addCartToMemory();
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
        <div class="totalPrice">$${item.price * item.quantity}</div>
        <div class="quantity">
            <span class="minus"><</span>
            <span>${item.quantity}</span>
            <span class="plus">></span>
        </div>
        `;
            listCartHTML.appendChild(newItem);
        })
    }
    iconCartSpan.innerText = totalQuantity;
}

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
        addCartToMemory();
    }
}
