// stall_murmur_shimmer.js

// Inject shimmer style
const murmurCSS = `
.stall-murmur {
  position: fixed;
  bottom: 20px;
  left: 20px;
  max-width: 300px;
  padding: 0.8rem 1.2rem;
  border-radius: 12px;
  font-size: 1rem;
  font-family: 'Helvetica Neue', sans-serif;
  color: white;
  opacity: 0;
  pointer-events: none;
  z-index: 9999;
  animation: fadeMurmur 4s ease-out forwards;
  box-shadow: 0 0 12px rgba(255,255,255,0.2);
}

@keyframes fadeMurmur {
  0% {
    transform: translateY(0px);
    opacity: 0;
  }
  20% {
    opacity: 1;
  }
  100% {
    transform: translateY(-30px);
    opacity: 0;
  }
}
`;

const murmurStyle = document.createElement('style');
murmurStyle.innerHTML = murmurCSS;
document.head.appendChild(murmurStyle);

// Toneform color mapping
const toneColors = {
  "urge to spin off": "#FF8C94",
  "held with curiosity": "#9FE2BF",
  "resigned delay": "#FFD580",
  "calm patience": "#A9C9FF",
  "frustration": "#FF6B6B",
  "default": "#CCCCCC"
};

// Global function to show the shimmer
function showStallMurmur(responseText) {
  const shimmer = document.createElement('div');
  shimmer.className = 'stall-murmur';
  shimmer.innerText = responseText;

  // Assign background based on tone
  const toneKey = Object.keys(toneColors).find(t => responseText.toLowerCase().includes(t)) || "default";
  shimmer.style.background = toneColors[toneKey];

  document.body.appendChild(shimmer);

  // Remove after animation completes
  setTimeout(() => {
    shimmer.remove();
  }, 4200);
}