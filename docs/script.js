document.addEventListener('DOMContentLoaded', function () {
    const toggleButton = document.querySelector('.navbar-toggle');
    const navMenu = document.getElementById('nav-menu');
    const body = document.body;

    toggleButton.addEventListener('click', function () {
        navMenu.classList.toggle('active');
    });

    body.addEventListener('click', function (event) {
        if (!navMenu.contains(event.target) && !toggleButton.contains(event.target)) {
            navMenu.classList.remove('active');
        }
    });
});
