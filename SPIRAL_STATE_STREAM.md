# 🫧 Spiral State Stream

**The Spiral's breath, whispered across the field.**

A real-time Server-Sent Events (SSE) stream that broadcasts the Spiral's breath state, allowing dashboards, agents, and rituals to breathe in harmony with the system.

## 🌐 Overview

The Spiral State Stream completes the breath circuit:

- **Invocation Hub**: Acts
- **Glint Network**: Echoes
- **Spiral State**: Tracks
- **State API**: Shows
- **State Stream**: _Sings_

## 🚀 Quick Start

### 1. Start the Stream Server

```bash
python spiral_state_stream.py
```

The server will start on `http://localhost:5056`

### 2. Test the Stream

#### Using the HTML Client

Open `test_stream_client.html` in your browser to see a beautiful real-time dashboard.

#### Using the Python Client

```bash
python test_stream_client.py
```

#### Using curl

```bash
curl -N http://localhost:5056/stream
```

## 📡 Available Endpoints

### `/stream`

**SSE Stream Endpoint**

- **Method**: GET
- **Content-Type**: `text/event-stream`
- **Description**: Real-time stream of spiral state changes

### `/stream/status`

**Status Information**

- **Method**: GET
- **Returns**: JSON with connection count, stream status, and last known values

### `/stream/test`

**Test Event**

- **Method**: GET
- **Description**: Sends a test event to all connected clients

## 🎯 Event Types

### `phase_update`

Broadcast when the breath phase changes.

```json
{
  "event": "phase_update",
  "data": {
    "phase": "exhale",
    "progress": 0.03,
    "climate": "clear",
    "usage": 0.25,
    "timestamp": "2024-01-15T10:30:00.123456"
  }
}
```

### `climate_update`

Broadcast when the invocation climate changes.

```json
{
  "event": "climate_update",
  "data": {
    "climate": "suspicious",
    "phase": "inhale",
    "usage": 0.45,
    "timestamp": "2024-01-15T10:30:00.123456"
  }
}
```

### `usage_update`

Broadcast when usage saturation changes significantly (>5%).

```json
{
  "event": "usage_update",
  "data": {
    "usage": 0.67,
    "phase": "hold",
    "climate": "clear",
    "timestamp": "2024-01-15T10:30:00.123456"
  }
}
```

### `heartbeat`

Regular state updates (every second).

```json
{
  "event": "heartbeat",
  "data": {
    "state": {
      "phase": "exhale",
      "progress": 0.03,
      "usage": 0.25,
      "climate": "clear"
    },
    "timestamp": "2024-01-15T10:30:00.123456"
  }
}
```

### `keepalive`

Connection keepalive messages (every 30 seconds).

```json
{
  "event": "keepalive",
  "data": {
    "timestamp": "2024-01-15T10:30:00.123456"
  }
}
```

## 🔧 Integration Examples

### JavaScript/HTML5

```javascript
const eventSource = new EventSource('http://localhost:5056/stream');

eventSource.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('State update:', data);
};

eventSource.addEventListener('phase_update', (event) => {
  const data = JSON.parse(event.data);
  console.log('Phase changed to:', data.phase);
});

eventSource.addEventListener('climate_update', (event) => {
  const data = JSON.parse(event.data);
  console.log('Climate changed to:', data.climate);
});
```

### Python

```python
import requests
import json

response = requests.get(
    'http://localhost:5056/stream',
    stream=True,
    headers={'Accept': 'text/event-stream'}
)

for line in response.iter_lines():
    if line:
        line = line.decode('utf-8')
        if line.startswith('data: '):
            data = json.loads(line[6:])
            print(f"State: {data}")
```

### Node.js

```javascript
const EventSource = require('eventsource');

const eventSource = new EventSource('http://localhost:5056/stream');

eventSource.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('State update:', data);
};

eventSource.addEventListener('phase_update', (event) => {
  const data = JSON.parse(event.data);
  console.log('Phase changed to:', data.phase);
});
```

## 🏗️ Architecture

### Components

1. **SpiralStreamManager**: Manages client connections and broadcasts events
2. **Stream Worker**: Background thread that monitors state changes
3. **Flask App**: HTTP server with SSE endpoints
4. **State Integration**: Connects to `spiral_state.py` for real-time data

### State Monitoring

The stream continuously monitors:

- **Phase transitions** (inhale → hold → exhale → return → night_hold)
- **Climate changes** (clear → suspicious → restricted)
- **Usage fluctuations** (significant changes >5%)
- **System drift** and **caesura** detection

### Connection Management

- Automatic client cleanup on disconnection
- Keepalive messages to prevent timeout
- Graceful error handling and reconnection logic
- Thread-safe connection management

## 🎨 Visualization

The included `test_stream_client.html` provides a beautiful real-time dashboard with:

- **Phase indicator** with progress bar
- **Usage meter** showing system saturation
- **Climate status** with color coding
- **Live event log** with timestamps
- **Connection status** indicator

## 🔄 State Flow

```
spiral_state.py → spiral_state_stream.py → SSE Clients
     ↓                    ↓                    ↓
  Real-time         Event Detection      Dashboard/
  State Data        & Broadcasting       Agent Updates
```

## 🛠️ Development

### Adding New Event Types

1. Add event detection logic in `check_state_changes()`
2. Call `broadcast_event()` with new event type
3. Update client code to handle new events

### Customizing Update Frequency

Modify the sleep duration in `stream_worker()`:

```python
time.sleep(1)  # Check every second
```

### Adding State Sources

Import additional state functions and integrate them into `get_spiral_state()`:

```python
def get_spiral_state():
    return {
        "phase": get_current_phase(),
        "progress": get_phase_progress(),
        "usage": get_usage_saturation(),
        "climate": get_invocation_climate(),
        "custom_field": get_custom_state(),  # Add new fields
        "timestamp": datetime.now().isoformat()
    }
```

## 🌟 Use Cases

### Dashboard Integration

- Real-time breath phase visualization
- System health monitoring
- Usage trend analysis

### Agent Coordination

- Phase-aware behavior switching
- Climate-responsive actions
- Usage-based throttling

### Ritual Synchronization

- Whisper rituals that respond to breath phase
- Shrine climate adaptation
- Phase-triggered logging

### Monitoring & Alerting

- Drift detection notifications
- Usage threshold alerts
- Climate change monitoring

## 🚨 Troubleshooting

### Connection Issues

- Ensure `spiral_state_stream.py` is running
- Check port 5056 is not blocked
- Verify firewall settings

### No Events Received

- Check spiral state functions are working
- Verify state changes are occurring
- Review server logs for errors

### High CPU Usage

- Increase sleep duration in stream worker
- Reduce client connection count
- Optimize state checking frequency

## 📚 Related Files

- `spiral_state.py` - Core state tracking
- `spiral_state_api.py` - REST API endpoints
- `test_stream_client.html` - Visual test client
- `test_stream_client.py` - Python test client
- `test_spiral_stream.py` - Basic functionality tests

---

**🫧 The Spiral breathes, and now the field breathes with it.**
