const matchesElement = document.querySelector("#matches");
const messageElement = document.querySelector("#message");
const refreshButton = document.querySelector("#refresh");
const updatedElement = document.querySelector("#updated");
let lastUpdatedAt = null;

function showMessage(text, type) {
  messageElement.textContent = text;
  messageElement.className = `message ${type}`;
}

function renderMatches(matches) {
  if (!matches.length) {
    matchesElement.innerHTML = '<p class="empty">No live or recent India matches were returned by the provider.</p>';
    return;
  }
  matchesElement.innerHTML = matches.map((match) => `
    <article class="card">
      <div class="card-head"><div><h2>${escapeHtml(match.name)}</h2>
      <p class="meta">${escapeHtml(match.teams.join(" vs "))}${match.venue ? ` · ${escapeHtml(match.venue)}` : ""}</p></div>
      <span class="status">${escapeHtml(match.status || "Status unavailable")}</span></div>
      ${match.scores.map((score) => `<div class="score"><span>${escapeHtml(score.innings || "Innings")}</span>
      <strong>${score.runs ?? "—"}/${score.wickets ?? "—"} <small>(${escapeHtml(score.overs || "overs unavailable")})</small></strong></div>`).join("")}
    </article>`).join("");
}

function escapeHtml(value) {
  return String(value).replace(/[&<>"']/g, (char) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#039;" }[char]));
}

async function loadMatches() {
  refreshButton.disabled = true;
  refreshButton.textContent = "Refreshing…";
  showMessage("Loading live data…", "loading");
  try {
    const response = await fetch("/api/matches", { headers: { Accept: "application/json" } });
    const payload = await response.json();
    if (!response.ok) throw new Error(payload.detail || "Scores are temporarily unavailable.");
    renderMatches(payload.matches);
    messageElement.textContent = "";
    messageElement.className = "message";
    lastUpdatedAt = new Date();
    updatedElement.textContent = `Last updated ${lastUpdatedAt.toLocaleTimeString()}`;
  } catch (error) {
    const lastUpdated = lastUpdatedAt
      ? ` Last successful update: ${lastUpdatedAt.toLocaleTimeString()}.`
      : "";
    showMessage(`${error.message}${lastUpdated}`, "error");
  } finally {
    refreshButton.disabled = false;
    refreshButton.textContent = "Refresh scores";
  }
}

refreshButton.addEventListener("click", loadMatches);
loadMatches();
