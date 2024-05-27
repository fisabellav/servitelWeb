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