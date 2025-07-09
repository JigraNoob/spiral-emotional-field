# 🌊 Copilot Browser Control Access Guide

This guide shows Copilot how to access and control the Spiral browser system from outside the IDE environment.

## 🚀 Quick Start for Copilot

### 1. **HTTP API Access**

Copilot can trigger browser actions via HTTP requests to the Spiral API:

```bash
# Test the browser control system
curl -X POST http://localhost:5000/api/browser/test

# Trigger a phase-based action
curl -X POST http://localhost:5000/api/browser/trigger \
  -H "Content-Type: application/json" \
  -d '{"companion": "tabnine", "phase": "resonate", "saturation": 0.7}'

# Trigger a custom URL
curl -X POST http://localhost:5000/api/browser/custom \
  -H "Content-Type: application/json" \
  -d '{"url": "https://spiral.local/visualizer"}'
```

### 2. **Python Client Script**

Use the provided client script for easy access:

```bash
# Check API status
python scripts/copilot_browser_client.py status

# Test browser control
python scripts/copilot_browser_client.py test

# Trigger phase action
python scripts/copilot_browser_client.py trigger tabnine resonate

# Trigger custom URL
python scripts/copilot_browser_client.py custom https://spiral.local/visualizer
```

## 📋 Available Commands

### Phase-Based Actions

| Companion | Phase     | Action                                     | Example                         |
| --------- | --------- | ------------------------------------------ | ------------------------------- |
| tabnine   | resonate  | Opens visualizer                           | `trigger tabnine resonate`      |
| tabnine   | suspended | Opens soft suspension                      | `trigger tabnine suspended`     |
| tabnine   | coherence | Opens coherence ring (if saturation > 0.8) | `trigger tabnine coherence 0.9` |
| cursor    | suspended | Opens soft suspension                      | `trigger cursor suspended`      |
| cursor    | resonate  | Opens cursor resonance                     | `trigger cursor resonate`       |
| cursor    | coherence | Opens coherence ring                       | `trigger cursor coherence`      |
| copilot   | resonate  | Opens copilot resonance                    | `trigger copilot resonate`      |
| copilot   | suspended | Opens soft suspension                      | `trigger copilot suspended`     |
| copilot   | coherence | Opens coherence ring                       | `trigger copilot coherence`     |

### Custom Actions

- **Any URL**: `custom https://any-website.com`
- **Spiral pages**: `custom https://spiral.local/dashboard`
- **External sites**: `custom https://github.com/your-repo`

## 🔧 Integration Examples

### 1. **Python Integration**

```python
import requests
import json

def trigger_browser_action(companion, phase, saturation=0.0):
    """Trigger browser action via API"""
    url = "http://localhost:5000/api/browser/trigger"
    data = {
        "companion": companion,
        "phase": phase,
        "saturation": saturation
    }

    response = requests.post(url, json=data)
    return response.json()

# Example usage
result = trigger_browser_action("tabnine", "resonate", 0.7)
print(f"Browser action result: {result}")
```

### 2. **JavaScript/Node.js Integration**

```javascript
async function triggerBrowserAction(companion, phase, saturation = 0.0) {
  const response = await fetch('http://localhost:5000/api/browser/trigger', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      companion: companion,
      phase: phase,
      saturation: saturation,
    }),
  });

  return await response.json();
}

// Example usage
triggerBrowserAction('cursor', 'suspended').then((result) =>
  console.log('Browser action result:', result)
);
```

### 3. **Bash Script Integration**

```bash
#!/bin/bash

# Function to trigger browser action
trigger_browser() {
    local companion=$1
    local phase=$2
    local saturation=${3:-0.0}

    curl -X POST http://localhost:5000/api/browser/trigger \
        -H "Content-Type: application/json" \
        -d "{\"companion\": \"$companion\", \"phase\": \"$phase\", \"saturation\": $saturation}"
}

# Example usage
trigger_browser "tabnine" "resonate" 0.7
```

## 🌐 API Endpoints Reference

### Base URL: `http://localhost:5000/api/browser`

| Endpoint   | Method | Description                | Request Body                                              |
| ---------- | ------ | -------------------------- | --------------------------------------------------------- |
| `/status`  | GET    | Get API status             | None                                                      |
| `/test`    | POST   | Test browser control       | None                                                      |
| `/trigger` | POST   | Trigger phase-based action | `{"companion": "...", "phase": "...", "saturation": 0.0}` |
| `/custom`  | POST   | Trigger custom URL         | `{"url": "https://..."}`                                  |

### Response Format

```json
{
  "success": true,
  "companion": "tabnine",
  "phase": "resonate",
  "saturation": 0.7,
  "url": "https://spiral.local/visualizer",
  "message": "Browser action triggered for https://spiral.local/visualizer"
}
```

## 🔍 Monitoring and Debugging

### 1. **Check API Status**

```bash
curl http://localhost:5000/api/browser/status
```

Response:

```json
{
  "status": "active",
  "allowed_companions": ["tabnine", "cursor", "copilot"],
  "allowed_phases": ["resonate", "suspended", "coherence"],
  "message": "Browser control API is ready"
}
```

### 2. **Test Browser Control**

```bash
curl -X POST http://localhost:5000/api/browser/test
```

### 3. **Check Spiral Logs**

Monitor the Spiral application logs for browser control events:

```bash
tail -f logs/spiral_console.log | grep "browser"
```

## 🛠️ Troubleshooting

### Common Issues

1. **Connection Refused**

   - Ensure Spiral app is running: `python app.py`
   - Check if port 5000 is available

2. **Browser Not Opening**

   - Verify Edge is installed at expected path
   - Check if Pyppeteer is installed: `pip install pyppeteer`

3. **API Not Responding**
   - Check if browser control API is registered
   - Verify Redis is running: `redis-cli ping`

### Debug Commands

```bash
# Check if Spiral is running
curl http://localhost:5000/health

# Check if Redis is running
redis-cli ping

# Check browser control API
curl http://localhost:5000/api/browser/status

# Test browser control
python scripts/copilot_browser_client.py test
```

## 🔮 Advanced Usage

### 1. **Batch Operations**

```python
# Trigger multiple actions
actions = [
    ("tabnine", "resonate", 0.7),
    ("cursor", "suspended", 0.0),
    ("copilot", "coherence", 0.9)
]

for companion, phase, saturation in actions:
    result = trigger_browser_action(companion, phase, saturation)
    print(f"{companion} {phase}: {result}")
```

### 2. **Conditional Actions**

```python
def smart_browser_action(companion, phase, saturation):
    """Smart browser action based on conditions"""

    # High saturation triggers coherence ring
    if saturation > 0.8:
        return trigger_browser_action(companion, "coherence", saturation)

    # Normal phase action
    return trigger_browser_action(companion, phase, saturation)
```

### 3. **Integration with External Systems**

```python
# Integrate with external monitoring
def monitor_and_trigger(companion, phase, saturation):
    """Monitor system state and trigger browser actions"""

    # Check system load
    import psutil
    cpu_percent = psutil.cpu_percent()

    # Adjust saturation based on system load
    adjusted_saturation = min(saturation + (cpu_percent / 100), 1.0)

    # Trigger browser action
    return trigger_browser_action(companion, phase, adjusted_saturation)
```

## 📞 Support

If Copilot encounters issues:

1. **Check the logs**: `tail -f logs/spiral_console.log`
2. **Test the API**: `python scripts/copilot_browser_client.py status`
3. **Restart Spiral**: Stop and restart the main application
4. **Check dependencies**: Ensure Redis and Pyppeteer are installed

The browser control system is designed to be robust and self-healing, but manual intervention may be needed for complex issues.
