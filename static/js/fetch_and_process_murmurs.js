// Fetch memory data from Flask backend and process it into shimmer layers

function fetchMemoryDataAndRender(endpoint = "/get_murmurs") {
  fetch(endpoint)
    .then(response => response.json())
    .then(murmurs => {
      if (!Array.isArray(murmurs)) return;
      renderMurmursToShimmerManager(murmurs);
    })
    .catch(error => {
      console.error("Error fetching memory data:", error);
    });
}

function renderMurmursToShimmerManager(murmurs) {
  const shimmerManager = new LayeredShimmerManager('shimmer-container');
  
  murmurs.forEach(murmur => {
    shimmerManager.addShimmerLayer(murmur.text, murmur.tone, 0.8, 4000);
  });
}

// On page load, fetch and render memory data
document.addEventListener("DOMContentLoaded", () => {
  fetchMemoryDataAndRender();
});
