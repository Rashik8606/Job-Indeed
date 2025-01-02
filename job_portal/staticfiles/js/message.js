function addMessage(sender, text, className) {
    const messageElement = document.createElement("div");
    messageElement.className = className;
    messageElement.style.marginBottom = "10px";
    messageElement.innerHTML = `<strong>${sender}:</strong> ${text}`;
    messagesContainer.appendChild(messageElement);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}


const messagesContainer = document.getElementById("chatbotMessages");

        function sendMessage() {
            const input = document.getElementById("chatbotInput");
            const message = input.value.trim();

            if (message) {
                // Add user message to chat
                addMessage("You", message, "user-message");

                // Simulate bot response
                setTimeout(() => {
                    addMessage("Bot", "Thanks for reaching out! How can I assist you?", "bot-message");
                }, 1000);

                // Clear input
                input.value = "";
            }
        }