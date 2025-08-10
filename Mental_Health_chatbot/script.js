// Authentication check
if (!localStorage.getItem('isLoggedIn')) {
    alert('Please login to access the chatbot.');
    window.location.href = '../login.html';
}

const inputStart = document.getElementById("input-start");
const sendStart = document.getElementById("send-start");
const inputChat = document.getElementById("input-chat");
const sendChat = document.getElementById("send-chat");
const chatStart = document.getElementById("chat-start");
const chatContent = document.getElementById("chat-content");
const messageArea = document.getElementById("message-area");
const chatList = document.getElementById("chat-list");


const newChatBtn = document.getElementById("new-chat-btn");

let activeChatId = null;
let selectedLang = "en"; // default

// Language Selection
document.querySelectorAll(".language-select").forEach(selector => {
  selector.value = selectedLang; // Set initial value
  selector.addEventListener("change", function () {
    selectedLang = this.value;
    console.log("Selected language:", selectedLang);
  });
});

// Create message bubble
function createBubble(text, sender, timestamp = null) {
  const bubble = document.createElement("div");
  bubble.classList.add("chat-bubble", sender === "user" ? "user-bubble" : "bot-bubble");
  bubble.innerText = text;

  const time = document.createElement("div");
  time.className = "timestamp";
  time.innerText = timestamp || new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  bubble.appendChild(time);

  messageArea.appendChild(bubble);
  messageArea.scrollTop = messageArea.scrollHeight;
}

// Save message to localStorage
function saveMessage(text, sender) {
  const allChats = JSON.parse(localStorage.getItem("chats") || "{}");
  if (!activeChatId) {
    activeChatId = Date.now().toString();
    allChats[activeChatId] = [];
  }
  allChats[activeChatId].push({
    text,
    sender,
    time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
  });
  localStorage.setItem("chats", JSON.stringify(allChats));
}

// Load conversation
function loadChat(id) {
  const allChats = JSON.parse(localStorage.getItem("chats") || "{}");
  const thread = allChats[id];
  if (!thread) return;

  messageArea.innerHTML = "";
  chatStart.style.display = "none";
  chatContent.style.display = "flex";
  activeChatId = id;

  thread.forEach(({ text, sender, time }) => createBubble(text, sender, time));
}

// Update chat list
function updateChatList() {
  const allChats = JSON.parse(localStorage.getItem("chats") || "{}");
  chatList.innerHTML = "";

  Object.entries(allChats).forEach(([id, messages]) => {
    if (messages.length === 0) return;

    const title = messages[0].text;
    const wrapper = document.createElement("div");
    wrapper.className = "chat-item";

    const input = document.createElement("input");
    input.value = title;
    input.onchange = () => {
      messages[0].text = input.value;
      localStorage.setItem("chats", JSON.stringify(allChats));
    };

    const del = document.createElement("button");
    del.innerText = "🗑";
    del.onclick = (e) => {
      e.stopPropagation();
      delete allChats[id];
      localStorage.setItem("chats", JSON.stringify(allChats));
      updateChatList();
    };

    wrapper.onclick = () => loadChat(id);
    wrapper.appendChild(input);
    wrapper.appendChild(del);
    chatList.appendChild(wrapper);
  });
}

// Send message to Flask backend using POST
async function sendMessageToBackend(message) {
  try {
    const response = await fetch("http://127.0.0.1:5000/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message: message, lang: selectedLang }),
    });

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }

    const data = await response.json();
    console.log("Backend response:", data);

    if (data.response) {
      createBubble(data.response, "bot");
      saveMessage(data.response, "bot");
    } else {
      createBubble("⚠️ No response from server.", "bot");
      saveMessage("⚠️ No response from server.", "bot");
    }
    updateChatList();
  } catch (error) {
    console.error("Error from backend:", error);
    createBubble("⚠️ Unable to connect to server.", "bot");
    saveMessage("⚠️ Unable to connect to server.", "bot");
    updateChatList();
  }
}

// Handle sending with backend call
function handleSend(inputElement) {
  const text = inputElement.value.trim();
  if (!text) return;

  createBubble(text, "user");
  saveMessage(text, "user");
  inputElement.value = "";

  const typing = document.createElement("div");
  typing.className = "chat-bubble bot-bubble";
  typing.innerText = "Typing...";
  messageArea.appendChild(typing);
  messageArea.scrollTop = messageArea.scrollHeight;

  sendMessageToBackend(text).finally(() => typing.remove());
}

// Voice Input
if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
  const SpeechRecognition = window.webkitSpeechRecognition || window.SpeechRecognition;
  
  document.querySelectorAll(".mic-btn").forEach(btn => {
    btn.onclick = () => {
      const recog = new SpeechRecognition();
      recog.continuous = false;
      recog.interimResults = false;
      recog.lang = selectedLang === "ta" ? "ta-IN" : "en-US";

      // Show "Listening..." bubble
      const listeningBubble = document.createElement("div");
      listeningBubble.className = "chat-bubble bot-bubble";
      listeningBubble.innerText = "🎤 Listening...";
      messageArea.appendChild(listeningBubble);
      messageArea.scrollTop = messageArea.scrollHeight;

      recog.start();

      recog.onresult = (event) => {
        if (event.results.length > 0) {
          const transcript = event.results[0][0].transcript.trim();
          const input = btn.closest(".chat-input").querySelector("input");
          
          if (transcript) {
            input.value = transcript;
            console.log("Voice transcript:", transcript);
            
            // Auto-send the transcribed text
            handleSend(input);
          }
        }
        
        if (listeningBubble.parentNode) {
          listeningBubble.remove();
        }
      };

      recog.onerror = (event) => {
        console.error("Speech recognition error:", event.error);
        
        if (listeningBubble.parentNode) {
          listeningBubble.remove();
        }
        
        let errorMsg = "⚠️ Voice input failed.";
        if (event.error === 'not-allowed') {
          errorMsg = "⚠️ Microphone access denied. Please allow microphone access.";
        } else if (event.error === 'no-speech') {
          errorMsg = "⚠️ No speech detected. Try again.";
        }
        
        createBubble(errorMsg, "bot");
      };

      recog.onend = () => {
        if (listeningBubble.parentNode) {
          listeningBubble.remove();
        }
      };
    };
  });
} else {
  // Hide mic buttons if speech recognition not supported
  document.querySelectorAll(".mic-btn").forEach(btn => {
    btn.style.display = "none";
  });
  console.warn("Speech recognition not supported in this browser");
}
// Send Events
sendStart.onclick = () => {
  chatStart.style.display = "none";
  chatContent.style.display = "flex";
  inputChat.value = inputStart.value;
  handleSend(inputStart);
};
sendChat.onclick = () => handleSend(inputChat);
inputStart.addEventListener("keydown", (e) => e.key === "Enter" && sendStart.click());
inputChat.addEventListener("keydown", (e) => e.key === "Enter" && sendChat.click());

// New Chat
newChatBtn.onclick = () => {
  messageArea.innerHTML = "";
  inputStart.value = "";
  inputChat.value = "";
  chatStart.style.display = "block";
  chatContent.style.display = "none";
  activeChatId = null;
};

// Daily Check-in
function dailyCheckIn() {
  const today = new Date().toDateString();
  const lastCheck = localStorage.getItem("lastCheckIn");
  if (lastCheck !== today) {
    localStorage.setItem("lastCheckIn", today);
    setTimeout(() => {
      createBubble("Hi 👋 How are you feeling today?", "bot");
      saveMessage("Hi 👋 How are you feeling today?", "bot");
    }, 800);
  }
}

// Theme toggle
function toggleTheme() {
  const body = document.body;
  body.classList.toggle("light-mode");
  const mode = body.classList.contains("light-mode") ? "light" : "dark";
  localStorage.setItem("theme", mode);
}
document.getElementById("theme-toggle").onclick = toggleTheme;

// Apply saved theme on load
window.addEventListener("DOMContentLoaded", () => {
  const savedTheme = localStorage.getItem("theme");
  if (savedTheme === "light") {
    document.body.classList.add("light-mode");
  }
});

// Export chat
function exportChat() {
  const bubbles = document.querySelectorAll(".chat-bubble");
  let text = "";
  bubbles.forEach(b => {
    const role = b.classList.contains("user-bubble") ? "You" : "Bot";
    text += `${role}: ${b.textContent.trim()}\n`;
  });
  const blob = new Blob([text], { type: "text/plain" });
  const link = document.createElement("a");
  link.href = URL.createObjectURL(blob);
  link.download = "chat.txt";
  link.click();
}

// On Load
window.onload = () => {
  updateChatList();
  const allChats = JSON.parse(localStorage.getItem("chats") || "{}");
  const lastId = Object.keys(allChats).pop();
  if (lastId) loadChat(lastId);
  dailyCheckIn();
};

function updateLogoByTheme() {
  const isLight = document.body.classList.contains("light-mode");
  document.getElementById("logo").src = isLight ? "Logo.png" : "Logo.png";
} 