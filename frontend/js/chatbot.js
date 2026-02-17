// --- API Base URL ---
// For production (deployed on Railway/Render/Fly.io):
const API_BASE = "https://public-scheme-navigator-production.up.railway.app/api";

// For local testing (FastAPI running on 127.0.0.1:8000):
// const API_BASE = "http://127.0.0.1:8000/api";

// --- Guidance Form Submission ---
document.getElementById("guidance-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const scheme = document.getElementById("scheme").value;

  try {
    const res = await fetch(`${API_BASE}/guidance?scheme=${encodeURIComponent(scheme)}`);
    if (!res.ok) throw new Error("Network response was not ok");
    const data = await res.json();

    const resultsDiv = document.getElementById("guidance-results");
    resultsDiv.innerHTML = `
      <h3>Required Documents for ${data.scheme}</h3>
      <ul>
        ${data.documents.map(doc => `<li>${doc}</li>`).join("")}
      </ul>
    `;
  } catch (error) {
    console.error("Error fetching guidance:", error);
    document.getElementById("guidance-results").innerText =
      "⚠️ Error fetching guidance from backend.";
  }
});
