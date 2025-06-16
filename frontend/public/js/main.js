document.addEventListener("DOMContentLoaded", function () {
    // Check if the user is authenticated
    const token = localStorage.getItem("token");
    if (!token) {
        showAuthModal();
        return;
    }

    // Add event listeners
    document.getElementById("pdfUpload").addEventListener("change", uploadPDF);
    document.getElementById("sendMessage").addEventListener("click", sendMessage);

    // Enter key support
    document.getElementById("userInput").addEventListener("keypress", function(e) {
        if (e.key === "Enter") {
            sendMessage();
        }
    });
});

// Modal functions
function showAuthModal() {
    document.getElementById("authModal").style.display = "flex";
}

function showSuccess(title, message) {
    document.getElementById("successTitle").textContent = title;
    document.getElementById("successMessage").textContent = message;
    document.getElementById("successModal").style.display = "flex";
}

function showError(title, message) {
    document.getElementById("errorTitle").textContent = title;
    document.getElementById("errorMessage").textContent = message;
    document.getElementById("errorModal").style.display = "flex";
}

function hideModal(modalId) {
    document.getElementById(modalId).style.display = "none";
}

// Loading spinner
function showLoading() {
    document.getElementById("loadingSpinner").style.display = "flex";
}

function hideLoading() {
    document.getElementById("loadingSpinner").style.display = "none";
}

// PDF upload function
async function uploadPDF() {
    const fileInput = document.getElementById("pdfUpload");
    if (fileInput.files.length === 0) {
        showError("Upload Error", "Please select a PDF file.");
        return;
    }

    showLoading();

    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    try {
        const response = await fetch("/api/upload_pdf", {
            method: "POST",
            body: formData,
            headers: {
                "Authorization": `Bearer ${localStorage.getItem("token")}`
            }
        });

        const data = await response.json();

        if (response.ok && data.pdf_id) {
            localStorage.setItem("pdf_id", data.pdf_id);
            showSuccess("Upload Successful", "PDF uploaded successfully!");
            // Clear file input
            fileInput.value = "";
        } else {
            showError("Upload Failed", data.detail || "Unknown error occurred during upload.");
        }
    } catch (error) {
        console.error("Upload Error:", error);
        showError("Upload Error", "Error uploading PDF. Please try again.");
    } finally {
        hideLoading();
    }
}

// Send message function
async function sendMessage() {
    const userInput = document.getElementById("userInput");
    const message = userInput.value.trim();
    const pdfId = localStorage.getItem("pdf_id");

    if (!message) {
        showError("Message Error", "Please enter a message.");
        return;
    }

    if (!pdfId) {
        showError("PDF Required", "Please upload a PDF first.");
        return;
    }

    showLoading();

    try {
        // Add user message to chat
        addMessageToChat(message, "user");
        userInput.value = "";

        const response = await fetch(`/api/chat_with_pdf/${pdfId}?user_message=${encodeURIComponent(message)}`, {
            method: "POST",
            headers: {
                "Authorization": `Bearer ${localStorage.getItem("token")}`
            }
        });

        const data = await response.json();

        if (response.ok) {
            addMessageToChat(data.message, "ai");
        } else {
            showError("Chat Error", data.detail || "Unknown error occurred during chat.");
        }
    } catch (error) {
        console.error("Chat Error:", error);
        showError("Network Error", "Error communicating with AI. Please check your connection.");
    } finally {
        hideLoading();
    }
}

// Helper function to add messages to chat
function addMessageToChat(text, sender) {
    const chatOutput = document.getElementById("chat-output");
    const messageDiv = document.createElement("div");
    messageDiv.className = `message ${sender}-message`;

    // Limit very long words by inserting zero-width spaces every 20 chars
    const formattedText = text.replace(/(.{20})/g, "$1\u200B");

    const avatar = sender === "user"
        ? document.getElementById("user-avatar").src
        : document.getElementById("ai-avatar").src;

    const senderName = sender === "user" ? "You" : "AI Assistant";

    messageDiv.innerHTML = sender === "user"
        ? `
            <img src="${avatar}" class="message-avatar" alt="${senderName}">
            <div class="message-content">
                <div class="message-sender">${senderName}</div>
                        <div class="message-text">${formattedText}</div>
            </div>
        `
        : `
            <div class="message-content">
                <div class="message-sender">${senderName}</div>
                <div class="message-text">${formattedText}</div>
            </div>
            <img src="${avatar}" class="message-avatar" alt="${senderName}">
        `;

    chatOutput.appendChild(messageDiv);
    chatOutput.scrollTop = chatOutput.scrollHeight;
}

// Logout function
function logout() {
    localStorage.removeItem("token");
    localStorage.removeItem("pdf_id");
    showSuccess("Logged Out", "You have been logged out successfully.");
    setTimeout(() => {
        window.location.href = "index.html";
    }, 1500);
}
