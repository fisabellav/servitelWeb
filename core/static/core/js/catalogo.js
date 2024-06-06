const filterGroups = document.querySelectorAll('.filter-group');

filterGroups.forEach(filterGroup => {
    const filterGroupTitle = filterGroup.querySelector('.filter-group-title');
    const filterGroupToggle = filterGroupTitle.querySelector('.filter-group-toggle');
    const filterOptions = filterGroup.querySelector('.filter-options');

    filterGroupToggle.addEventListener('click', () => {
        filterGroup.classList.toggle('active');
    });
});

const priceRange = document.querySelector('#price-range');
const priceLabelMin = document.querySelector('#price-label-min');
const priceLabelMax = document.querySelector('#price-label-max');

priceRange.addEventListener('input', () => {
    console.log("holaa")
    const minPrice = priceRange.value;
    const maxPrice = priceRange.max;
    const labelMin = `$${minPrice}`;
    const labelMax = `$${maxPrice}`;

    priceLabelMin.textContent = labelMin;
    priceLabelMax.textContent = labelMax;
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