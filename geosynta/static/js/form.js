// Get the form elements
const locationInput = document.getElementById('location');
const dateInput = document.getElementById('date');
const submitButton = document.querySelector('input[type="submit"]');
const resultMessage = document.getElementById('resultMessage');

// Function to enable/disable the submit button based on input values
function checkFormFields() {
    if (locationInput.value && dateInput.value) {
        submitButton.disabled = false;
    } else {
        submitButton.disabled = true;
    }
}

// Add event listeners to check the form fields on input
locationInput.addEventListener('input', checkFormFields);
dateInput.addEventListener('input', checkFormFields);

// Handle form submission
document.getElementById('dataForm').addEventListener('submit', function(e) {
    e.preventDefault();

    // Collect form data
    const formData = new FormData();
    formData.append('location', locationInput.value);
    formData.append('date', dateInput.value);

    // Send the form data to the server via AJAX
    fetch('/predict', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        // Display submission result below the form
        resultMessage.textContent = data.message;

        // Clear form fields (optional)
        locationInput.value = '';
        dateInput.value = '';
        
        // Disable the submit button again until fields are filled
        submitButton.disabled = true;
    })
    .catch(error => {
        resultMessage.textContent = "An error occurred: " + error;
    });
});
