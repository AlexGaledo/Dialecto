document.addEventListener("DOMContentLoaded", function () {
    setTimeout(() => {
        document.getElementById("loading-screen").style.display = "none";
        document.getElementById("main-content").style.display = "block";
        document.getElementById("messages-section").style.display = "block";
        document.body.style.backgroundColor = "#7ED5FF";
    }, 3000);
});

document.addEventListener("DOMContentLoaded", function () {
    const footerButtons = document.querySelectorAll(".footer-section");
    const sections = document.querySelectorAll(".section-content");

    function showSection(sectionId) {
        sections.forEach(section => {
            section.style.display = "none";
        });

        document.getElementById(sectionId).style.display = "block";

        if (sectionId === "messages-section") {
            document.body.style.backgroundColor = "#7ED5FF";
        } else {
            document.body.style.backgroundColor = "transparent";
        }
    }

    footerButtons.forEach(button => {
        button.addEventListener("click", function () {
            const section = this.getAttribute("data-section") + "-section";
            showSection(section);
        });
    });
});

document.getElementById('login-form').addEventListener('submit', function() {
    document.getElementById('message').classList.remove('hidden');
});



// Code from original HTML

function sendMessage() {
    let userInput = document.getElementById("user_input").value;
    let chatBox = document.getElementById("chatbox");

    if (!userInput.trim()) {
        return; // Prevent empty messages
    }

    // Append user's message to chatbox
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
            chatBox.innerHTML += `<p><strong>Chatbot:</strong> ${data.chatbot_response}</p>`;
        }
        chatBox.scrollTop = chatBox.scrollHeight; // Auto-scroll to latest message
    })
    .catch(error => {
        chatBox.innerHTML += `<p style="color:red;"><strong>Error:</strong> ${error}</p>`;
    });

    // Clear input field
    document.getElementById("user_input").value = "";
}

function getMicrophoneInput() {
    fetch("/microphone", { method: "POST" })
        .then(response => response.json())
        .then(data => {
            document.getElementById("text").value = data.text;
            sendMessage(); // Automatically send the recognized text for translation
        })
        .catch(error => console.error("Error:", error));
}
