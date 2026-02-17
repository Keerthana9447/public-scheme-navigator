// --- API Base URL ---
// For production (deployed on Railway/Render/Fly.io):
// const API_BASE = "https://public-scheme-navigator-production.up.railway.app/api";

// For local testing (FastAPI running on 127.0.0.1:8000):
const API_BASE = "http://127.0.0.1:8000/api";

// --- Add message to chat window ---
function addMessage(text, sender) {
  const chatContainer = document.getElementById("chat-container");
  const msgDiv = document.createElement("div");
  msgDiv.classList.add("chat-message", sender);
  msgDiv.innerText = text;
  chatContainer.appendChild(msgDiv);
  chatContainer.scrollTop = chatContainer.scrollHeight;
}

// --- Typing indicator control ---
function showTyping() {
  document.getElementById("typing-indicator").classList.remove("hidden");
}
function hideTyping() {
  document.getElementById("typing-indicator").classList.add("hidden");
}

// --- Function to send message ---
async function sendMessage() {
  const queryInput = document.getElementById("query");
  const query = queryInput.value.trim();
  const age = document.getElementById("chat-age")?.value;
  const income = document.getElementById("chat-income")?.value;
  if (!query) return;

  addMessage(query, "user");
  showTyping();

  const url = new URL(`${API_BASE}/chat`);
  url.searchParams.append("query", query);
  if (age) url.searchParams.append("age", age);
  if (income) url.searchParams.append("income", income);

  try {
    const res = await fetch(url);
    if (!res.ok) throw new Error("Network response was not ok");
    const data = await res.json();
    hideTyping();
    addMessage(data.response, "bot");
  } catch (error) {
    console.error("Error fetching response:", error);
    hideTyping();
    addMessage("⚠️ Error fetching response from backend.", "bot");
  }

  queryInput.value = "";
}

// --- Button click ---
document.getElementById("ask-btn").addEventListener("click", sendMessage);

// --- Keyboard support (Enter key) ---
document.getElementById("query").addEventListener("keydown", (event) => {
  if (event.key === "Enter") {
    event.preventDefault();
    sendMessage();
  }
});
