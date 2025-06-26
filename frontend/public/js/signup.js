document.addEventListener("DOMContentLoaded", function () {
    const signupForm = document.getElementById("signupForm");
    const successMessage = document.getElementById("successMessage");
    const spinner = document.getElementById("spinner");
    const submitBtn = document.getElementById("submitBtn");

    signupForm.addEventListener("submit", async function (event) {
        event.preventDefault();

        const username = document.getElementById("username").value;
        const password = document.getElementById("password").value;

        // Show loading spinner
        spinner.style.display = "block";
        submitBtn.style.display = "none";

        try {
            const response = await fetch("/api/signup", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ username, password }),
            });

            const data = await response.json();

            if (response.ok) {
                // Show beautiful success message
                successMessage.style.display = "flex";

                // Optional: Auto-redirect after 3 seconds
                setTimeout(() => {
                    window.location.href = "login.html";
                }, 3000);
            } else {
                // Show error message
                alert("Signup failed: " + (data.detail || "Unknown error"));
            }
        } catch (error) {
            console.error("Signup Error:", error);
            alert("Error during signup. Please try again.");
        } finally {
            // Hide loading spinner
            spinner.style.display = "none";
            submitBtn.style.display = "block";
        }
    });
});
