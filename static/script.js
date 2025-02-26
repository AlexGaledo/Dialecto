document.addEventListener("DOMContentLoaded", function () {
    // Hide loading screen and show main content after 3 seconds
    setTimeout(() => {
        const loadingScreen = document.getElementById("loading-screen");
        const mainContent = document.getElementById("main-content");
        const messagesSection = document.getElementById("messages-section");

        if (loadingScreen) loadingScreen.style.display = "none";
        if (mainContent) mainContent.style.display = "block";
        if (messagesSection) messagesSection.style.display = "block";

        document.body.style.backgroundColor = "#7ED5FF";
    }, 3000);

    // Handle footer button navigation
    const footerButtons = document.querySelectorAll(".footer-section");
    const sections = document.querySelectorAll(".section-content");

    function showSection(sectionId) {
        sections.forEach(section => section.style.display = "none");

        const targetSection = document.getElementById(sectionId);
        if (targetSection) targetSection.style.display = "block";

        document.body.style.backgroundColor = sectionId === "messages-section" ? "#7ED5FF" : "transparent";
    }

    footerButtons.forEach(button => {
        button.addEventListener("click", function () {
            const section = this.getAttribute("data-section") + "-section";
            showSection(section);
        });
    });

    // Handle login form submission (check if element exists)
    const loginForm = document.getElementById("login-form");
    if (loginForm) {
        loginForm.addEventListener("submit", function () {
            const message = document.getElementById("message");
            if (message) message.classList.remove("hidden");
        });
    }
});

// Function to send message to chatbot
function sendMessage() {
    let userInput = document.getElementById("user_input").value;
    let chatBox = document.getElementById("chatbox");

    if (!userInput.trim()) return; // Prevent empty messages

    // Append user's message
    chatBox.innerHTML += `<p><strong>You:</strong> ${userInput}</p>`;

    // Send input to chatbot
    fetch("/chatbot", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: userInput })
    })
    .then(response => response.json())
    .then(data => {
        console.log("Server Response:", data); // Debugging

        if (data.error) {
            chatBox.innerHTML += `<p style="color:red;"><strong>Error:</strong> ${data.error}</p>`;
        } else {
            chatBox.innerHTML += `<p><strong>Translation:</strong> ${data.translated_text}</p>`;

            // Properly format chatbot response with line breaks
            let formattedResponse = data.chatbot_response.replace(/\n/g, "<br>");
            chatBox.innerHTML += `<p><strong>Chatbot:</strong> ${formattedResponse}</p>`;
        }

        chatBox.scrollTop = chatBox.scrollHeight; // Auto-scroll
    })
    .catch(error => {
        chatBox.innerHTML += `<p style="color:red;"><strong>Error:</strong> ${error}</p>`;
    });

    // Clear input field
    document.getElementById("user_input").value = "";
}


// Function to get microphone input and send it to chatbot
function getMicrophoneInput() {
    fetch("/microphone", { method: "POST" })
        .then(response => response.json())
        .then(data => {
            const textInput = document.getElementById("text");
            if (textInput) {
                textInput.value = data.text;
                sendMessage(); // Automatically send the recognized text
            }
        })
        .catch(error => console.error("Error:", error));
}

