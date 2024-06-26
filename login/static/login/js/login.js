function clearForm() {
    document.getElementById("email_login").value = "";
    document.getElementById("password_login").value = "";
}

// Configura el evento onclick del botón Clear
document.addEventListener("DOMContentLoaded", function() {
    var clearButton = document.getElementById("clearButton");
    if (clearButton) {
        clearButton.onclick = function() {
            clearForm();
        };
    }
});