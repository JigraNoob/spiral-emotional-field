---
globs:
  - dashboard_phase_tracker.py
  - dashboard_visualization.html
description: Integrate WebSocket for real-time event emission
alwaysApply: true
---

# WebSocket Integration

In dashboard_phase_tracker.py, add WebSocket emission using flask-socketio to emit 'glint_event' with event type and payload. In dashboard_visualization.html, add a JavaScript WebSocket listener to receive 'glint_event' and call updateSpiral(data.payload.arm).

```html
// ... existing code ...

<script>
  const socket = new WebSocket("ws://localhost:5000");
  socket.onmessage = function(event) {
    const data = JSON.parse(event.data);
    if (data.type === 'glint_event' && data.payload.arm) {
      updateSpiral(data.payload.arm);
    }
  };

  function updateSpiral(arm) {
    // ... your existing updateSpiral logic ...
  }
</script>

// ... existing code ...
```
