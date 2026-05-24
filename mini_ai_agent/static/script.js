function goToChat() {
  document.getElementById("landing").classList.add("hidden");
  document.getElementById("chat-page").classList.remove("hidden");
}

function goBack() {
  document.getElementById("chat-page").classList.add("hidden");
  document.getElementById("landing").classList.remove("hidden");
}

async function clearChat() {
  await fetch("/clear", { method: "POST" });

  document.getElementById("messages").innerHTML = `
    <div class="greeting-banner">
      <div class="g-title">Hello, I'm MINNIE 👋</div>
      <div class="g-sub">Powered by Gemini · Always ready to help</div>
    </div>
  `;
}

async function sendMessage() {
  const input = document.getElementById("user-input");
  const messages = document.getElementById("messages");
  const message = input.value.trim();

  if (message === "") return;

  messages.innerHTML += `
    <div class="msg user">
      <div class="msg-avatar">🧑</div>
      <div class="msg-bubble">${message}</div>
    </div>
  `;
  input.value = "";
  messages.scrollTop = messages.scrollHeight;

  messages.innerHTML += `
    <div class="msg bot" id="loading-msg">
      <div class="msg-avatar">🤖</div>
      <div class="msg-bubble">...</div>
    </div>
  `;

  try {
    const response = await fetch("/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: message })
    });

    const data = await response.json();


    document.getElementById("loading-msg")?.remove();
    messages.innerHTML += `
      <div class="msg bot">
        <div class="msg-avatar">🤖</div>
        <div class="msg-bubble markdown">${marked.parse(data.reply)}</div>
      </div>
    `;
  } catch (err) {
    document.getElementById("loading-msg")?.remove();
    messages.innerHTML += `
      <div class="msg bot">
        <div class="msg-avatar">🤖</div>
        <div class="msg-bubble">❌ Something went wrong. Please try again.</div>
      </div>
    `;
  }

  messages.scrollTop = messages.scrollHeight;
}

document.getElementById("user-input").addEventListener("keydown", function (event) {
  if (event.key === "Enter" && !event.shiftKey) {
    event.preventDefault();
    sendMessage();
  }
});