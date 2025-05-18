document.addEventListener("DOMContentLoaded", function () {
    const loginForm = document.getElementById("loginForm");
    const successMessage = document.getElementById("successMessage");
    const errorMessage = document.getElementById("errorMessage");
    const errorModalText = document.getElementById("errorModalText");
    const spinner = document.getElementById("spinner");
    const submitBtn = document.getElementById("submitBtn");
    const usernameError = document.getElementById("usernameError");
    const passwordError = document.getElementById("passwordError");

    loginForm.addEventListener("submit", async function (event) {
        event.preventDefault();

        // Reset error messages
        usernameError.style.display = "none";
        passwordError.style.display = "none";

        const username = document.getElementById("username").value;
        const password = document.getElementById("password").value;

        // Validate inputs
        if (!username) {
            usernameError.textContent = "Username is required";
            usernameError.style.display = "block";
            return;
        }

        if (!password) {
            passwordError.textContent = "Password is required";
            passwordError.style.display = "block";
            return;
        }

        // Show loading spinner
        spinner.style.display = "block";
        submitBtn.style.display = "none";

        try {
            const response = await fetch("http://127.0.0.1:8000/token", {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                },
                body: `username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}`,
            });

            const data = await response.json();

            if (response.ok) {
                localStorage.setItem("token", data.access_token);
                
                // Show beautiful success message
                successMessage.style.display = "flex";
                
                // Auto-redirect after 2 seconds
                setTimeout(() => {
                    window.location.href = "main.html";
                }, 2000);
            } else {
                // Show specific error message
                const errorMsg = data.detail || "Invalid username or password";
                
                // Show error modal
                errorModalText.textContent = errorMsg;
                errorMessage.style.display = "flex";
                
                // Also show inline errors if relevant
                if (errorMsg.toLowerCase().includes("username")) {
                    usernameError.textContent = errorMsg;
                    usernameError.style.display = "block";
                } else if (errorMsg.toLowerCase().includes("password")) {
                    passwordError.textContent = errorMsg;
                    passwordError.style.display = "block";
                }
            }
        } catch (error) {
            console.error("Login Error:", error);
            errorModalText.textContent = "Network error. Please try again.";
            errorMessage.style.display = "flex";
        } finally {
            // Hide loading spinner
            spinner.style.display = "none";
            submitBtn.style.display = "block";
        }
    });

    // Clear error messages when typing
    document.getElementById("username").addEventListener("input", () => {
        usernameError.style.display = "none";
    });
    document.getElementById("password").addEventListener("input", () => {
        passwordError.style.display = "none";
    });
});