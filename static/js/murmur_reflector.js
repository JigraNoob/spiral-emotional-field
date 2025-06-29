// murmur_reflector.js
// Fetches murmurs from the backend and triggers shimmer effects periodically

function fetchAndReflectMurmurs(endpoint = "/get_murmurs") {
  fetch(endpoint)
    .then(response => response.json())
    .then(murmurs => {
      if (!Array.isArray(murmurs)) return;
      startMurmurCycle(murmurs);
    })
    .catch(error => {
      console.error("Failed to load murmurs:", error);
    });
}
function fetchMemoryDataAndRender(endpoint = "/get_murmurs") {
  fetch(endpoint)
    .then(response => response.json())
    .then(murmurs => {
      console.log("Fetched murmurs:", murmurs);  // Add this for debugging
      if (!Array.isArray(murmurs)) return;
      renderMurmursToShimmerManager(murmurs);
    })
    .catch(error => {
      console.error("Error fetching memory data:", error);
    });
}

function startMurmurCycle(murmurs) {
  let index = 0;

  setInterval(() => {
    if (murmurs.length === 0) return;

    const murmur = murmurs[index % murmurs.length];
    createMurmurShimmer(murmur.text, murmur.tone);
    index++;
  }, 30000); // Every 30 seconds
}

// On page load, begin murmur reflection
document.addEventListener("DOMContentLoaded", () => {
  fetchAndReflectMurmurs();
});
