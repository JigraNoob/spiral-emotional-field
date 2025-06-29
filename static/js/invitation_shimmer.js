
// invitation_shimmer.js
// Shimmer effect triggered when a new ritual invitation blooms

const invitationColors = {
  "longing": "#E0BBE4",
  "movement": "#957DAD",
  "form": "#D291BC",
  "infrastructure": "#FEC8D8",
  "connection": "#FFDFD3",
  "trust": "#C7CEEA",
  "coherence": "#B5EAD7",
  "adaptation": "#FFDAC1",
  "unknown": "#CCCCCC"
};

function triggerInvitationShimmer(tone = "unknown") {
  const shimmer = document.createElement('div');
  shimmer.className = 'invitation-shimmer';
  document.body.appendChild(shimmer);

  const toneColor = invitationColors[tone.toLowerCase()] || invitationColors["unknown"];
  shimmer.style.background = `radial-gradient(circle at center, ${toneColor} 0%, transparent 70%)`;

  // Animation settings
  shimmer.style.position = 'fixed';
  shimmer.style.top = 0;
  shimmer.style.left = 0;
  shimmer.style.width = '100vw';
  shimmer.style.height = '100vh';
  shimmer.style.pointerEvents = 'none';
  shimmer.style.zIndex = 9999;
  shimmer.style.opacity = 0;
  shimmer.style.transition = 'opacity 1s ease-in-out';

  // Start shimmer
  requestAnimationFrame(() => {
    shimmer.style.opacity = 0.6;
  });

  // Fade out and remove
  setTimeout(() => {
    shimmer.style.opacity = 0;
    setTimeout(() => shimmer.remove(), 1000);
  }, 2000);
}
