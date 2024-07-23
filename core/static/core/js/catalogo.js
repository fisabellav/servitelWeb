



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