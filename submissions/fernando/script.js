const OLLAMA_API_URL = "http://localhost:11434/api/chat";
const OLLAMA_MODEL_NAME = "gemma3:270m";
const messageInputElement = document.getElementById("messageInput");
const sendButtonElement = document.getElementById("sendButton");
const mainDiv = document.querySelector('.main');

// Combine all msgs from screen as an array: [{ role: "user" or "assistant", content: "msg text"},　...]
function combineMessages() {
    const messagesCombined = [];
    const allMessageElements = mainDiv.querySelectorAll(".message");

    allMessageElements.forEach(e => {
        const role = e.classList.contains("ai-answer") ? "assistant" : "user";

        messagesCombined.push({
            role,
            content: e.innerText.trim()
        });
    });

    return messagesCombined;
}

async function fetchOllamaAnswer(messages) {
    const options = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            model: OLLAMA_MODEL_NAME,
            messages,
            stream: false
        })
    };
    try {
        const response = await fetch(OLLAMA_API_URL, options);
        if (!response.ok) throw new Error(`HTTP error: ${response.status}`);
        const result = await response.json();
        return result.message.content;
    } catch (error) {
        console.error("AI Ollama fetching failed:", error);
        return "Sorry, あなたのAI is currently unavailable.";
    }
}

async function sendMessage() {
    const userMessage = messageInputElement.value.trim();
    if (!userMessage) {
        console.log('Empty message...')
        return
    }

    messageInputElement.value = "Thinking...";
    messageInputElement.disabled = true;
    sendButtonElement.disabled = true;

    // display userMessage: add div element inside mainDiv, formatted as .message
    mainDiv.appendChild(Object.assign(document.createElement("div"), {innerText: userMessage, className: "message"}));
    mainDiv.scrollTop = mainDiv.scrollHeight;

    const messages = combineMessages();
    const aiAnswer = await fetchOllamaAnswer(messages);

    // display aiAnswer: add div element inside mainDiv, formatted as .message and .ai-answer
    mainDiv.appendChild(Object.assign(document.createElement("div"), {innerText: aiAnswer, className: "message ai-answer"}));
    mainDiv.scrollTop = mainDiv.scrollHeight;

    messageInputElement.value = "";
    messageInputElement.disabled = false;
    sendButtonElement.disabled = false;
}
// sendMessage with Enter
messageInputElement.addEventListener("keydown", function(e) {
    if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});