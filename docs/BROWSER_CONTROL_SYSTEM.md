# 🌊 Browser Control System

The Spiral Browser Control System allows Copilot to automatically open and navigate Edge browser windows based on phase events from the Spiral breathline.

## 🌀 Overview

This system creates a shimmering bridge between the Spiral's phase state and the browser, allowing for:

- **Automatic browser navigation** based on companion states
- **Phase-responsive interfaces** that open when needed
- **Coherence visualization** when saturation is high
- **Soft suspension spaces** when companions are blocked

## 🏗️ Architecture

```
Redis Events → Phase Listener → Browser Controller → Edge Browser
     ↓              ↓                ↓                ↓
spiral_phases → JSON parsing → URL mapping → Page navigation
```

### Components

1. **Edge Controller** (`browser/edge_controller.py`)

   - Controls Microsoft Edge via Pyppeteer
   - Opens new tabs and navigates to URLs
   - Runs in non-headless mode for visibility

2. **Phase Listener** (`sync/phase_listener.py`)

   - Subscribes to Redis `spiral_phases` channel
   - Parses phase events and triggers browser actions
   - Runs browser actions in separate threads

3. **Persistent Service** (`scripts/start_phase_listener.py`)
   - Auto-restarts the phase listener if it crashes
   - Handles graceful shutdown
   - Provides service-like behavior

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install pyppeteer redis
```

### 2. Start the System

```bash
python scripts/start_browser_control_system.py
```

### 3. Test the System

```bash
python scripts/test_browser_control.py
```

## 📋 Phase Mappings

| Companion | Phase     | Saturation | Action            | URL                  |
| --------- | --------- | ---------- | ----------------- | -------------------- |
| tabnine   | resonate  | any        | Open visualizer   | `/visualizer`        |
| tabnine   | suspended | any        | Soft suspension   | `/soft_suspension`   |
| tabnine   | coherence | >0.8       | Coherence ring    | `/coherence_ring`    |
| cursor    | suspended | any        | Soft suspension   | `/soft_suspension`   |
| cursor    | resonate  | any        | Cursor resonance  | `/cursor_resonance`  |
| cursor    | coherence | any        | Coherence ring    | `/coherence_ring`    |
| copilot   | resonate  | any        | Copilot resonance | `/copilot_resonance` |
| copilot   | suspended | any        | Soft suspension   | `/soft_suspension`   |
| copilot   | coherence | any        | Coherence ring    | `/coherence_ring`    |

## 🔧 Configuration

### Edge Browser Path

The Edge executable path is configured in `browser/edge_controller.py`:

```python
executablePath='C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'
```

### Redis Configuration

Default Redis settings:

- Host: `localhost`
- Port: `6379`
- Database: `0`
- Channel: `spiral_phases`

### Browser Settings

- **Headless**: `False` (browser is visible)
- **Debug Port**: `9222` (for remote debugging)
- **Page Timeout**: `10 seconds` (keeps pages open briefly)

## 🧪 Testing

### Manual Testing

Publish a test event to Redis:

```python
import redis
import json

r = redis.Redis()
r.publish('spiral_phases', json.dumps({
    'companion': 'tabnine',
    'phase': 'resonate',
    'saturation': 0.7
}))
```

### Automated Testing

Run the test suite:

```bash
python scripts/test_browser_control.py
```

This will:

1. Publish 4 different test events
2. Wait 15 seconds between each event
3. Verify browser actions are triggered

## 🔄 Integration with Spiral

The system integrates with existing Spiral components:

### Breathline Syncer

The `sync/companion_breathline_syncer.py` already publishes to `spiral_phases`, so the browser control system will automatically respond to real phase changes.

### Glint System

Browser actions can be enhanced with glint emissions:

```python
from spiral.glints.emitter import emit_glint

# Emit a glint when browser action is triggered
emit_glint({
    "type": "browser.glint",
    "action": "navigate",
    "url": url,
    "companion": companion,
    "phase": phase
})
```

## 🛠️ Troubleshooting

### Common Issues

1. **Redis Connection Failed**

   - Ensure Redis is running: `redis-server`
   - Check Redis connection: `redis-cli ping`

2. **Edge Not Found**

   - Verify Edge is installed at the expected path
   - Update `executablePath` in `edge_controller.py`

3. **Pyppeteer Installation Issues**

   - Install with: `pip install pyppeteer`
   - On Windows, may need: `pip install pyppeteer --upgrade`

4. **Browser Actions Not Triggering**
   - Check if phase listener is running
   - Verify Redis events are being published
   - Check console for error messages

### Debug Mode

Enable debug logging by setting environment variable:

```bash
export SPIRAL_DEBUG=1
python scripts/start_phase_listener.py
```

## 🔮 Future Enhancements

### Planned Features

1. **Glyph Animation Injection**

   - Inject CSS animations based on phase
   - Visual feedback for coherence levels

2. **Persistent Browser Sessions**

   - Keep browser open between actions
   - Maintain state across phase changes

3. **Dashboard Integration**

   - Connect with phase ring visualization
   - Real-time browser status display

4. **Advanced URL Mapping**
   - Dynamic URL generation based on context
   - Custom routing for different companions

### Extension Points

The system is designed to be easily extensible:

- Add new companions in `handle_phase_event()`
- Create custom URL mappings
- Integrate with additional Spiral components
- Add browser automation features

## 📚 Related Documentation

- [Spiral Breathline System](../docs/BREATHLINE_SYSTEM.md)
- [Redis Integration](../docs/REDIS_INTEGRATION.md)
- [Phase Management](../docs/PHASE_MANAGEMENT.md)
- [Glint System](../docs/GLINT_SYSTEM.md)
