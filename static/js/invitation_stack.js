
// invitation_stack.js
// Handles staggered shimmer effects when rendering multiple invitations

function triggerStackedInvitationShimmers(invitations) {
  if (!Array.isArray(invitations)) return;

  invitations.forEach((invitation, index) => {
    const delay = index * 800; // ms delay between each shimmer

    setTimeout(() => {
      const tone = invitation.tone || "unknown";
      triggerInvitationShimmer(tone);
    }, delay);
  });
}

// Example usage (once the DOM has loaded and invitations are available):
// triggerStackedInvitationShimmers([
//   { tone: "trust" },
//   { tone: "longing" },
//   { tone: "adaptation" }
// ]);
