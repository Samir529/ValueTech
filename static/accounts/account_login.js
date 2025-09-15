// Email and phone number pattern verification for account login.
document.getElementById("accountLoginForm").addEventListener("submit", function(event) {
    const usernameInput = document.getElementById("username").value.trim();

    // Email regex
    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    // Phone regex (10–14 digits, allows + at start)
    const phonePattern = /^\+?\d{10,14}$/;

    const errorDiv = document.getElementById("errorMessage");
    const errorText = document.getElementById("errorText");

    if (!emailPattern.test(usernameInput) && !phonePattern.test(usernameInput)) {
        event.preventDefault(); // stop form submission
        // Show the warning div
        errorDiv.style.display = "block";
        errorText.textContent = "Please enter a valid email address or phone number.";
    } else {
        errorDiv.style.display = "none"; // no error
    }
  });
