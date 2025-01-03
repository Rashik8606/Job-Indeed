
function toggleCheckbox() {
    const checkbox = document.getElementById('btncheck2');
    const submitButton = document.getElementById('submitBtn');
    
    // Toggle checkbox state
    checkbox.checked = !checkbox.checked;

    // Submit the form if checked
    if (checkbox.checked) {
        submitButton.click();
    }
}

