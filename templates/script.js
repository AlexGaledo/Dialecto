document.addEventListener("DOMContentLoaded", function () {
    setTimeout(() => {
        document.getElementById("loading-screen").style.display = "none";
        document.getElementById("main-content").style.display = "block";
    }, 3000);
});





// Code from original HTML

function getMicrophoneInput() {
    fetch("/microphone", { method: "POST" })
        .then(response => response.json())
        .then(data => {
            document.getElementById("text").value = data.text;
        })
        .catch(error => console.error("Error:", error));
}

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
        chatBox.innerHTML += `<p><strong>Chatbot:</strong> ${data.chatbot_response}</p>`;
        chatBox.scrollTop = chatBox.scrollHeight; // Auto-scroll to latest message
    })
    .catch(error => {
        chatBox.innerHTML += `<p style="color:red;"><strong>Error:</strong> ${error}</p>`;
    });

    // Clear input field
    document.getElementById("user_input").value = "";
}