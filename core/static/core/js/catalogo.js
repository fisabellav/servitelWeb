document.addEventListener('DOMContentLoaded', function () {
    const applyFiltersBtn = document.getElementById('apply-filters-btn');
    applyFiltersBtn.addEventListener('click', function () {
        const cameraFilter = document.getElementById('camera-filter');
        const channelFilter = document.getElementById('channel-filter');

        const selectedCameras = Array.from(cameraFilter.selectedOptions).map(option => option.value);
        const selectedChannels = Array.from(channelFilter.selectedOptions).map(option => option.value);

        const url = new URL(window.location.href);
        url.searchParams.delete('cameras');
        url.searchParams.delete('channels');

        selectedCameras.forEach(camera => url.searchParams.append('cameras', camera));
        selectedChannels.forEach(channel => url.searchParams.append('channels', channel));

        window.location.href = url.toString();
    });
});

document.addEventListener('DOMContentLoaded', function () {
    // Obtener todos los elementos con la clase .deseos
    const deseosElements = document.querySelectorAll('.deseos');

    deseosElements.forEach(deseos => {
        deseos.addEventListener('click', function () {
            let heart = this;
            let heartRect = heart.getBoundingClientRect();

            // Crear y clonar el corazón
            let heartClone = heart.cloneNode(true);
            heartClone.style.position = 'absolute';
            heartClone.style.left = `${heartRect.left + window.scrollX}px`;
            heartClone.style.top = `${heartRect.top + window.scrollY}px`;
            heartClone.style.width = `${heartRect.width}px`;
            heartClone.style.height = `${heartRect.height}px`;
            heartClone.style.zIndex = '1000';
            heartClone.style.transition = 'transform 1s, opacity 1s';

            document.body.appendChild(heartClone);

            // Obtener la posición del corazón en la barra de navegación
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
            let translateX = navbarRect.left + window.scrollX + (navbarRect.width / 2) - (heartRect.left + window.scrollX) - (heartRect.width / 2);
            let translateY = navbarRect.top + window.scrollY + (navbarRect.height / 2) - (heartRect.top + window.scrollY) - (heartRect.height / 2);
            // Aplicar estilos para la animación
            requestAnimationFrame(() => {
                heartClone.style.transform = `translate(${translateX}px, ${translateY}px)`;
                heartClone.style.opacity = '0';
            });

            heartClone.addEventListener('transitionend', function () {
                heartClone.remove();
                // Aquí puedes agregar cualquier lógica adicional después de la animación
            });
        });
    });
});

// Almacena la posición de desplazamiento antes de recargar la página
window.onbeforeunload = function () {
    localStorage.setItem('scrollPosition', window.pageYOffset);
};

// Restaura la posición de desplazamiento después de recargar la página
window.onload = function () {
    if (localStorage.getItem('scrollPosition')) {
        window.scrollTo(0, localStorage.getItem('scrollPosition'));
        localStorage.removeItem('scrollPosition');
    }
};