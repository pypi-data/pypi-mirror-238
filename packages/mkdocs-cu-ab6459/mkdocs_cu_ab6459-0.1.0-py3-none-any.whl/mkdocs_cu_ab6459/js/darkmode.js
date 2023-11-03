const checked = JSON.parse(localStorage.getItem("chkboxDarkMode"));
let checkbox = null;

$(document).ready(function() {
    checkbox = $('#chkboxDarkMode')[0];

    if (checked === true) {
        checkbox.checked = true;
        document.documentElement.setAttribute('data-bs-theme','dark')
        document.getElementById('dark-mode-icon').classList.add("bi-sun-fill")
    }

});

function darkmode() {
    if (document.documentElement.getAttribute('data-bs-theme') === 'dark') {
        checkbox.checked = false;
        localStorage.setItem("chkboxDarkMode", checkbox.checked);
        document.documentElement.setAttribute('data-bs-theme', 'light')
        document.getElementById('dark-mode-icon').classList.add("bi-moon-fill")
        document.getElementById('dark-mode-icon').classList.remove("bi-sun-fill")
    } else {
        checkbox.checked = true;
        localStorage.setItem("chkboxDarkMode", checkbox.checked);
        document.documentElement.setAttribute('data-bs-theme', 'dark')
        document.getElementById('dark-mode-icon').classList.remove("bi-moon-fill")
        document.getElementById('dark-mode-icon').classList.add("bi-sun-fill")
    }
}