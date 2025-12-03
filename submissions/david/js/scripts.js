let currentChatId = null;

async function getTxtValue() {
  const mainDiv = document.getElementById("mainDiv");
  const userValue = document.getElementById("txtAreaInput");

  const userTxtValue = userValue.value.trim();
  if (!userTxtValue) return;

  // show message from user
  const userTxtDiv = document.createElement("div");
  userTxtDiv.className = "user-txt-div";
  userTxtDiv.innerHTML = `<p>${escapeHtml(userTxtValue).replace(/\n/g, "<br>")}</p>`;
  mainDiv.appendChild(userTxtDiv);

  // AI placeholder + spinner
  const aiDiv = document.createElement("div");
  aiDiv.className = "ai-div";
  const spinner = document.createElement("div");
  spinner.className = "spinner";
  aiDiv.appendChild(spinner);
  mainDiv.appendChild(aiDiv);
  mainDiv.scrollTop = mainDiv.scrollHeight;

  // DATABASE: create chat if first message
  if (!currentChatId) {
    const chatTitle = userTxtValue.substring(0, 25) + "...";
    const res = await fetch("http://127.0.0.1:3000/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title: chatTitle })
    });
    const chatData = await res.json();
    currentChatId = chatData.id;
    // re-render chat list (opcional)
    renderChatList().catch(console.error);
  }

  // save user message to DB
  try {
    await fetch("http://127.0.0.1:3000/api/message", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        chat_id: currentChatId,
        role: "user",
        text: userTxtValue
      })
    });
  } catch (err) {
    console.error("Erro ao salvar mensagem do usuário:", err);
  }

  // send to AI service
  try {
    const response = await fetch("http://192.168.1.244:11434/api/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        model: "dolphin3:latest",
        prompt: userTxtValue,
        stream: false
      })
    });

    const data = await response.json();
    const aiResponse = data.response || "(no response)";

    // remove spinner and show AI text
    aiDiv.removeChild(spinner);
    const p = document.createElement("p");
    p.innerHTML = escapeHtml(aiResponse).replace(/\n/g, "<br>");
    aiDiv.appendChild(p);
    mainDiv.scrollTop = mainDiv.scrollHeight;

    // save AI message to DB
    try {
      await fetch("http://127.0.0.1:3000/api/message", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          chat_id: currentChatId,
          role: "ai",
          text: aiResponse
        })
      });
      // update chats (opcional)
      renderChatList().catch(console.error);
    } catch (err) {
      console.error("Error can't save IA message:", err);
    }

  } catch (err) {
    // network / fetch error
    console.error("Erro ao chamar AI:", err);
    if (aiDiv.contains(spinner)) aiDiv.removeChild(spinner);
    aiDiv.innerHTML = "<p>Error to connect AI server.</p>";
  }

  // clear input and focus
  userValue.value = "";
  userValue.focus();
}

// Render chat list (navbar)
async function renderChatList() {
  const chatList = document.getElementById("chatList");
  if (!chatList) return;
  const res = await fetch("http://127.0.0.1:3000/api/chats");
  const chats = await res.json();
  chatList.innerHTML = "";
  chats.forEach(chat => {
    const item = document.createElement("div");
    item.className = "chat-item";
    item.textContent = chat.title;
    item.onclick = () => loadChatIntoScreen(chat.id);
    chatList.appendChild(item);
  });
}

// Load a chat and render messages
async function loadChatIntoScreen(chatId) {
  currentChatId = chatId;
  const mainDiv = document.getElementById("mainDiv");
  mainDiv.innerHTML = "";
  const res = await fetch(`http://127.0.0.1:3000/api/chat/${chatId}`);
  const messages = await res.json(); // <-- use () !
  messages.forEach(msg => {
    const div = document.createElement("div");
    div.className = msg.role === "user" ? "user-txt-div" : "ai-div";
    div.innerHTML = `<p>${escapeHtml(msg.text).replace(/\n/g, "<br>")}</p>`;
    mainDiv.appendChild(div);
  });
  mainDiv.scrollTop = mainDiv.scrollHeight;
}

// small helper to avoid XSS when inserting text
function escapeHtml(text) {
  return String(text)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

// expose function to window so onclick inline works
window.getTxtValue = getTxtValue;

// run initial render
window.addEventListener("load", () => {
  renderChatList().catch(console.error);
});
