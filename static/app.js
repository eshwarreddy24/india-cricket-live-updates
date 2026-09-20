const statusElement = document.getElementById("status");
const liveContainer = document.getElementById("live-matches");
const recentContainer = document.getElementById("recent-matches");
const form = document.getElementById("team-form");
const teamInput = document.getElementById("team");

function setStatus(message) {
  statusElement.textContent = message;
}

function renderMatches(container, matches) {
  container.innerHTML = "";

  if (!matches.length) {
    container.innerHTML = '<p class="empty">No matches available from provider.</p>';
    return;
  }

  for (const match of matches) {
    const inningsHtml = (match.innings || [])
      .map((item) => `<li>${item.inning}: ${item.runs ?? "-"}/${item.wickets ?? "-"} (${item.overs ?? "-"} overs)</li>`)
      .join("");

    const el = document.createElement("article");
    el.className = "card";
    el.innerHTML = `
      <h3>${match.name}</h3>
      <p><strong>Teams:</strong> ${(match.teams || []).join(" vs ") || "Unavailable"}</p>
      <p><strong>Status:</strong> ${match.status || "Unavailable"}</p>
      <p><strong>Type:</strong> ${match.match_type || "Unknown"}</p>
      <p><strong>Venue:</strong> ${match.venue || "Unavailable"}</p>
      <p><strong>Date:</strong> ${match.date || "Unavailable"}</p>
      <ul class="innings">${inningsHtml || "<li>Scorecard details unavailable from provider.</li>"}</ul>
    `;
    container.appendChild(el);
  }
}

async function loadMatches(team = "India") {
  setStatus("Loading matches...");

  const configResponse = await fetch("/api/config");
  const configData = await configResponse.json();

  if (!configData.configured) {
    setStatus(configData.message);
    renderMatches(liveContainer, []);
    renderMatches(recentContainer, []);
    return;
  }

  try {
    const response = await fetch(`/api/matches?team=${encodeURIComponent(team)}`);
    const data = await response.json();

    if (!response.ok) {
      setStatus(data.message || "Provider error while loading matches.");
      renderMatches(liveContainer, []);
      renderMatches(recentContainer, []);
      return;
    }

    setStatus(`Showing data from ${data.provider}.`);
    renderMatches(liveContainer, data.live_matches || []);
    renderMatches(recentContainer, data.recent_matches || []);
  } catch (error) {
    setStatus("Network error while loading live updates.");
  }
}

form.addEventListener("submit", (event) => {
  event.preventDefault();
  const team = teamInput.value.trim();

  if (!/^[A-Za-z ]{2,30}$/.test(team)) {
    setStatus("Enter a valid team name (letters and spaces only).");
    return;
  }

  loadMatches(team);
});

loadMatches();
