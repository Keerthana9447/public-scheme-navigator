// --- API Base URL ---
// For production (deployed on Railway/Render/Fly.io):
// const API_BASE = "https://public-scheme-navigator-production.up.railway.app/api";

// For local testing (FastAPI running on 127.0.0.1:8000):
const API_BASE = "http://127.0.0.1:8000/api";

// --- Navigation Handling ---
document.querySelectorAll(".nav-link").forEach(link => {
  link.addEventListener("click", (e) => {
    e.preventDefault();
    const target = e.target.getAttribute("data-target");

    // Hide all sections
    document.querySelectorAll(".section").forEach(sec => sec.classList.add("hidden"));

    // Show the selected section
    document.getElementById(target).classList.remove("hidden");
  });
});
