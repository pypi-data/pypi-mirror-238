document.addEventListener('DOMContentLoaded', () => {
    const navElements = document.querySelectorAll('.navbar-item, .has-dropdown');
    navElements.forEach(el => {
        el.addEventListener('mousedown', toggleNavDropDown);
        el.addEventListener('blur', deactivateNavDropDown);
    })
})


function toggleNavDropDown() {
    const active = this.classList.toggle('is-active');
    if (active) {
        this.setAttribute('tabindex', '0');
    } else {
        this.removeAttribute('tabindex');
    }
}


function deactivateNavDropDown() {
    this.classList.remove('is-active');
    this.removeAttribute('tabindex');
}