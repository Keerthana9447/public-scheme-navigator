// --- API Base URL ---
// For production (deployed on Railway/Render/Fly.io):
// const API_BASE = "https://public-scheme-navigator-production.up.railway.app/api";

// For local testing (FastAPI running on 127.0.0.1:8000):
const API_BASE = "http://127.0.0.1:8000/api";

// --- Eligibility Form Submission ---
document.getElementById("eligibility-form").addEventListener("submit", async (event) => {
  event.preventDefault();

  const age = document.getElementById("age").value.trim();
  const income = document.getElementById("income").value.trim();
  const gender = document.getElementById("gender").value;
  const occupation = document.getElementById("occupation").value.trim();
  const scheme = document.getElementById("scheme").value;
  const disability = document.getElementById("disability").checked;

  const resultsDiv = document.getElementById("results");
  resultsDiv.innerText = "⏳ Checking eligibility...";

  try {
    const url = new URL(`${API_BASE}/eligibility`);
    url.searchParams.append("age", age);
    url.searchParams.append("income", income);
    if (gender) url.searchParams.append("gender", gender);
    if (occupation) url.searchParams.append("occupation", occupation);
    if (disability) url.searchParams.append("disability", "true");

    const res = await fetch(url);
    if (!res.ok) throw new Error("Network response was not ok");
    const data = await res.json();

    if (scheme && data.eligible_schemes.includes(scheme)) {
      resultsDiv.innerHTML = `
        <p>✅ You are eligible for:</p>
        <div class="badge-container">
          <span class="badge eligible">${scheme}</span>
        </div>
      `;
    } else if (scheme) {
      resultsDiv.innerHTML = `
        <p>❌ You are not eligible for:</p>
        <div class="badge-container">
          <span class="badge not-eligible">${scheme}</span>
        </div>
      `;
    } else {
      // Show all eligible schemes if no specific scheme was selected
      resultsDiv.innerHTML = `
        <p>${data.message}</p>
        <div class="badge-container">
          ${data.eligible_schemes.map(s => `<span class="badge eligible">${s}</span>`).join(" ")}
        </div>
      `;
    }
  } catch (error) {
    console.error("Error fetching eligibility:", error);
    resultsDiv.innerText = "⚠️ Error fetching eligibility from backend.";
  }
});
