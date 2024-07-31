document.addEventListener("DOMContentLoaded", function() {
    const alert = document.querySelector('.floating-alert');
    if (alert) {
        setTimeout(() => {
            // Use Bootstrap's alert method to close the alert
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 3000); // 3000ms = 3 seconds
    }
});