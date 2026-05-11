const API_BASE = window.API_BASE || "http://localhost:8000";

const healthBox = document.getElementById("healthBox");
const analyticsBox = document.getElementById("analyticsBox");
const moviesGrid = document.getElementById("moviesGrid");
const searchInput = document.getElementById("searchInput");
const genreSelect = document.getElementById("genreSelect");
const refreshBtn = document.getElementById("refreshBtn");

async function fetchJson(path) {
  const response = await fetch(`${API_BASE}${path}`);
  if (!response.ok) {
    throw new Error(`Request failed: ${response.status}`);
  }
  return response.json();
}

async function loadHealth() {
  try {
    const data = await fetchJson("/health");
    healthBox.textContent = JSON.stringify(data, null, 2);
  } catch (error) {
    healthBox.textContent = error.message;
  }
}

async function loadMovies() {
  const params = new URLSearchParams();
  if (searchInput.value) params.append("search", searchInput.value);
  if (genreSelect.value) params.append("genre", genreSelect.value);

  try {
    const movies = await fetchJson(`/movies?${params.toString()}`);
    moviesGrid.innerHTML = movies
      .map(
        (movie) => `
          <article class="card">
            <img src="${movie.thumbnail_url || "https://picsum.photos/500/300"}" alt="${movie.title}" />
            <div class="card-content">
              <h3>${movie.title}</h3>
              <p class="meta">${movie.genre} • ${movie.release_year} • ${movie.rating}/10</p>
              <p>${movie.description}</p>
              <button onclick="recordWatch(${movie.id})">Record Watch Event</button>
            </div>
          </article>
        `
      )
      .join("");
  } catch (error) {
    moviesGrid.innerHTML = `<p>${error.message}</p>`;
  }
}

async function loadAnalytics() {
  try {
    const data = await fetchJson("/analytics/top-movies");
    analyticsBox.textContent = JSON.stringify(data, null, 2);
  } catch (error) {
    analyticsBox.textContent = error.message;
  }
}

async function recordWatch(movieId) {
  await fetch(`${API_BASE}/watch-events`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      movie_id: movieId,
      user_id: "demo-user",
      seconds_watched: Math.floor(Math.random() * 600) + 60,
    }),
  });
  await loadAnalytics();
}

async function refreshAll() {
  await Promise.all([loadHealth(), loadMovies(), loadAnalytics()]);
}

searchInput.addEventListener("input", loadMovies);
genreSelect.addEventListener("change", loadMovies);
refreshBtn.addEventListener("click", refreshAll);

refreshAll();
