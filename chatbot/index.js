const chatBody = document.getElementById("chatBody");
const promptBox = document.getElementById("prompt-box");
const sendButton = document.getElementById("sendButton");

// Form geçerliliğini kontrol et
function validateForm() {
    const isPromptValid = promptBox.value.trim() !== "";
    sendButton.disabled = !isPromptValid;
    sendButton.style.opacity = isPromptValid ? "1" : "0.6";
}

promptBox.addEventListener("input", validateForm);

// Mesaj ekleme fonksiyonu
function addMessage(content, type) {
    const messageDiv = document.createElement("div");
    messageDiv.classList.add("message", type);
    messageDiv.textContent = content;
    chatBody.appendChild(messageDiv);
    chatBody.scrollTop = chatBody.scrollHeight;
}

// Kullanıcı mesajını ve yanıtı işleme
function sendRequest() {
    const userPrompt = promptBox.value.trim();

    if (userPrompt) {
        // Kullanıcı mesajını ekle
        addMessage(userPrompt, "user");
        promptBox.value = "";
        validateForm();

        // Bekleme mesajı ekle
        const waitingMessage = document.createElement("div");
        waitingMessage.classList.add("message", "bot");
        waitingMessage.textContent = "Bekleniyor...";
        chatBody.appendChild(waitingMessage);

        // Backend'e istek gönder
        fetch("https://web-integrated-chat-bot.onrender.com/proxy", { //Proxy API'si
            method: "POST",
            mode: "cors",
            headers: { "Content-Type": "application/json",
                "Accept": "application/json"
             },
             body: JSON.stringify({
                url: "https://web-integrated-chat-bot.onrender.com/generate", // Render API
                userPrompt: userPrompt
            }),
        })
        .then(response => response.json())
        .then(data => {
            chatBody.removeChild(waitingMessage); 

            if (data && data.status === "success" && data.response.trim()) {
                addMessage(data.response, "bot"); 
            } else {
                const testContent = data?.response ? data.response : "Boş içerik";
                addMessage(`İçerik boş geldi! Test mesajı: "${testContent} ve durum kodu: ${data.status}"`, "bot");
            }
        })
        .catch(() => {
            chatBody.removeChild(waitingMessage);
            addMessage("Bağlantı hatası! Lütfen daha sonra tekrar deneyin.", "bot");
        });
    }
}

sendButton.addEventListener("click", sendRequest);
promptBox.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
        sendRequest();
    }
});

