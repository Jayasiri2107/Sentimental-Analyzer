const form = document.getElementById("feedbackForm");
const input = document.getElementById("feedbackInput");
const charCount = document.getElementById("charCount");
const submitBtn = document.getElementById("submitBtn");
const wall = document.getElementById('feedbackWall');

input.addEventListener("input", () => {
  charCount.textContent = `${input.value.length} / 500`;
});

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const text = input.value.trim();
  if (!text) return;

  submitBtn.disabled = true;
  submitBtn.textContent = "Analyzing...";

  try {
    const response = await fetch("http://127.0.0.1:8000/messages", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text }),
    });

    if (!response.ok) {
      throw new Error(`Server responded with ${response.status}`);
    }

    const data = await response.json();
    addCard(data);
    form.reset();
    charCount.textContent = "0 / 500";
  } catch (err) {
    alert("Something went wrong. Please try again.");
    console.error("Submit error:", err);
  } finally {
    submitBtn.disabled = false;
    submitBtn.textContent = "Analyze Sentiment";
    input.focus();
  }
});

function addCard(data) {
  const sentimentConfig = {
    Positive: { color: '#7FA19D', emoji: 'emojis/happy.png' },
    Neutral:  { color: '#746D91', emoji: 'emojis/neutral.png' },
    Negative: { color: '#C4A193', emoji: 'emojis/sad.png' }
  };

  const config = sentimentConfig[data.sentiment] || sentimentConfig['Neutral'];
  const time = new Date(data.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

  const card = document.createElement('div');
  card.className = 'feedback-card';
  card.style.backgroundColor = config.color;
  card.innerHTML = `
    <div class="card-content">
      <p class="card-text">${data.text}</p>
      <span class="card-time">${time}</span>
    </div>
    <img class="card-emoji" src="${config.emoji}" alt="${data.sentiment}" />
  `;

  wall.prepend(card);
}

async function loadMessages() {
  try {
    const res = await fetch("http://127.0.0.1:8000/messages");
    const messages = await res.json();
    messages.forEach(addCard);
  } catch (err) {
    console.log('Backend not running yet:', err);
  }
}

loadMessages();