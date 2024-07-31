document.addEventListener('DOMContentLoaded', function () {
    const toggleBtn = document.querySelector('.toggle_btn');
    const toggleBtnIcon = document.querySelector('.toggle_btn i');
    const dropdownMenu = document.querySelector('.dropdown_menu');
    const dropdownItems = dropdownMenu.querySelectorAll('.nav-item');
    const maxHeight = dropdownItems.length * 46; // Assuming each item is 45px high, adjust as needed

    toggleBtn.onclick = function () {
        dropdownMenu.classList.toggle('open')
        const isOpen = dropdownMenu.classList.contains('open')

        toggleBtnIcon.classList = isOpen ? 'fa-solid fa-xmark' : 'fa-solid fa-bars'

        // Adjust max-height based on the number of items
        if (isOpen) {
            // Adjust max-height based on the number of items
            const dropdownOpen = document.querySelector('#navbarbody .dropdown_menu.open');
            dropdownOpen.style.height = `${maxHeight}px`;
        } else {
            dropdownMenu.style.height = '0';
        }
    };
});


function setNavbarBackgroundOnScroll(backgroundImageUrl) {
    const navbar = document.querySelector(".myNavbar");

    window.addEventListener("scroll", function () {
        if (window.scrollY > 80) {
            navbar.classList.add("scrolled");
            navbar.style.backgroundImage = `url('${backgroundImageUrl}')`;
        } else {
            navbar.classList.remove("scrolled");
            navbar.style.backgroundImage = "";
        }
    });
}

