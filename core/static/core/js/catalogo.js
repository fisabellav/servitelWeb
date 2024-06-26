const filterGroups = document.querySelectorAll('.filter-group');

filterGroups.forEach(filterGroup => {
    const filterGroupTitle = filterGroup.querySelector('.filter-group-title');
    const filterGroupToggle = filterGroupTitle.querySelector('.filter-group-toggle');
    const filterOptions = filterGroup.querySelector('.filter-options');

    filterGroupToggle.addEventListener('click', () => {
        filterGroup.classList.toggle('active');
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