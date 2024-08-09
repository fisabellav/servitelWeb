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

var swiper = new Swiper(".slide-container", {
    slidesPerView: 4,
    spaceBetween: 20,
    sliderPerGroup: 4,
    loop: true,
    centerSlide: "true",
    fade: "true",
    grabCursor: "true",
    pagination: {
        el: ".swiper-pagination",
        clickable: true,
        dynamicBullets: true,
    },
    navigation: {
        nextEl: ".swiper-button-next",
        prevEl: ".swiper-button-prev",
    },

    breakpoints: {
        0: {
            slidesPerView: 1,
        },
        520: {
            slidesPerView: 2,
        },
        768: {
            slidesPerView: 3,
        },
        1000: {
            slidesPerView: 4,
        },
    },
});



