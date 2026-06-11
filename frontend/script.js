const form = document.getElementById("feedbackForm");
const input = document.getElementById("feedbackInput");
const charCount = document.getElementById("charCount");
const submitBtn = document.getElementById("submitBtn");

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
    const response = await fetch("/messages", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text }),
    });

    if (!response.ok) {
      throw new Error(`Server responded with ${response.status}`);
    }

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
