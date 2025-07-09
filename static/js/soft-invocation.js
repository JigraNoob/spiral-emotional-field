class SoftInvocation {
  initializeArmTouches() {
    document.querySelectorAll('.spiral-arm').forEach((arm) => {
      arm.addEventListener('click', (e) => {
        const toneform = arm.dataset.toneform;
        this.whisperGlint(toneform, e);
      });
    });
  }

  whisperGlint(toneform, event) {
    // Create ripple effect from touch point
    this.createRipple(event.clientX, event.clientY);

    // Invoke glint through spiral
    fetch('/api/spiral/whisper', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        toneform: toneform,
        invocation_type: 'soft_touch',
        coordinates: { x: event.clientX, y: event.clientY },
      }),
    });
  }
}
