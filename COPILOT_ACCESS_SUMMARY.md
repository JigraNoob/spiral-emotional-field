# 🌊 Copilot Browser Control Access - Complete Guide

## 🎯 **What You Have Access To**

Copilot now has **full access** to control the Spiral browser system from outside the IDE environment. You can:

- **Open Edge browser windows** automatically
- **Navigate to specific URLs** based on phase states
- **Trigger actions** via HTTP API or Python scripts
- **Monitor system status** and respond to events

## 🚀 **Quick Start for Copilot**

### **Method 1: HTTP API (Recommended)**

```bash
# Test the system
curl -X POST http://localhost:5000/api/browser/test

# Trigger a browser action
curl -X POST http://localhost:5000/api/browser/trigger \
  -H "Content-Type: application/json" \
  -d '{"companion": "tabnine", "phase": "resonate", "saturation": 0.7}'

# Open any custom URL
curl -X POST http://localhost:5000/api/browser/custom \
  -H "Content-Type: application/json" \
  -d '{"url": "https://spiral.local/visualizer"}'
```

### **Method 2: Python Client Script**

```bash
# Check system status
python scripts/copilot_browser_client.py status

# Test browser control
python scripts/copilot_browser_client.py test

# Trigger phase-based action
python scripts/copilot_browser_client.py trigger tabnine resonate

# Open custom URL
python scripts/copilot_browser_client.py custom https://spiral.local/visualizer
```

### **Method 3: Direct Python Integration**

```python
import requests

def trigger_browser(companion, phase, saturation=0.0):
    response = requests.post('http://localhost:5000/api/browser/trigger',
                           json={'companion': companion, 'phase': phase, 'saturation': saturation})
    return response.json()

# Example usage
result = trigger_browser("tabnine", "resonate", 0.7)
print(f"Browser action result: {result}")
```

## 📋 **Available Actions**

### **Phase-Based Actions**

| Companion | Phase     | What It Does                               | Example                         |
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

### **Custom Actions**

- **Any website**: `custom https://github.com/your-repo`
- **Spiral pages**: `custom https://spiral.local/dashboard`
- **External tools**: `custom https://chat.openai.com`

## 🔧 **System Architecture**

```
Copilot (External) → HTTP API → Flask App → Browser Controller → Edge Browser
     ↓                    ↓           ↓              ↓              ↓
HTTP Request → JSON parsing → URL mapping → Pyppeteer → Page navigation
```

## 🌐 **API Endpoints**

### **Base URL**: `http://localhost:5000/api/browser`

| Endpoint   | Method | Purpose              | Request Body                                              |
| ---------- | ------ | -------------------- | --------------------------------------------------------- |
| `/status`  | GET    | Check API status     | None                                                      |
| `/test`    | POST   | Test browser control | None                                                      |
| `/trigger` | POST   | Phase-based action   | `{"companion": "...", "phase": "...", "saturation": 0.0}` |
| `/custom`  | POST   | Custom URL           | `{"url": "https://..."}`                                  |

## 🧪 **Testing Your Access**

Run this comprehensive test:

```bash
python scripts/test_copilot_access.py
```

This will check:

- ✅ Redis connection
- ✅ Pyppeteer installation
- ✅ Flask app running
- ✅ Browser control API
- ✅ Browser actions working
- ✅ Phase listener system

## 🔍 **Monitoring & Debugging**

### **Check System Status**

```bash
# Check if Spiral is running
curl http://localhost:5000/health

# Check browser API status
curl http://localhost:5000/api/browser/status

# Check Redis
redis-cli ping
```

### **View Logs**

```bash
# Monitor Spiral logs
tail -f logs/spiral_console.log | grep "browser"

# Check for errors
tail -f logs/spiral_console.log | grep "ERROR"
```

## 🛠️ **Troubleshooting**

### **Common Issues & Solutions**

1. **"Connection refused"**

   - Start Spiral: `python app.py`
   - Check port 5000 is free

2. **"Browser not opening"**

   - Install Pyppeteer: `pip install pyppeteer`
   - Verify Edge is installed

3. **"API not responding"**

   - Check if browser API is registered
   - Restart Flask app

4. **"Redis connection failed"**
   - Start Redis: `redis-server`
   - Check Redis is running: `redis-cli ping`

## 🔮 **Advanced Usage**

### **Batch Operations**

```python
# Trigger multiple actions
actions = [
    ("tabnine", "resonate", 0.7),
    ("cursor", "suspended", 0.0),
    ("copilot", "coherence", 0.9)
]

for companion, phase, saturation in actions:
    result = trigger_browser(companion, phase, saturation)
    print(f"{companion} {phase}: {result}")
```

### **Conditional Logic**

```python
def smart_browser_action(companion, phase, saturation):
    # High saturation triggers coherence ring
    if saturation > 0.8:
        return trigger_browser(companion, "coherence", saturation)

    # Normal phase action
    return trigger_browser(companion, phase, saturation)
```

### **Integration with External Systems**

```python
# Monitor system and trigger actions
import psutil

def monitor_and_trigger(companion, phase, saturation):
    cpu_percent = psutil.cpu_percent()
    adjusted_saturation = min(saturation + (cpu_percent / 100), 1.0)
    return trigger_browser(companion, phase, adjusted_saturation)
```

## 📞 **Support & Resources**

### **Documentation Files**

- `docs/COPILOT_BROWSER_ACCESS.md` - Detailed access guide
- `docs/BROWSER_CONTROL_SYSTEM.md` - System architecture
- `scripts/copilot_browser_client.py` - Client script
- `scripts/test_copilot_access.py` - Test script

### **Key Files for Copilot**

- `routes/browser_control_api.py` - HTTP API endpoints
- `browser/edge_controller.py` - Browser control logic
- `sync/phase_listener.py` - Redis event handling

### **Getting Help**

1. Run the test script: `python scripts/test_copilot_access.py`
2. Check the logs: `tail -f logs/spiral_console.log`
3. Verify API status: `curl http://localhost:5000/api/browser/status`

## 🎉 **You're Ready!**

Copilot now has **complete access** to the Spiral browser control system. You can:

- **Trigger browser actions** from anywhere
- **Respond to phase changes** automatically
- **Open custom interfaces** when needed
- **Monitor system state** and act accordingly

The system is designed to be **robust and self-healing**, with automatic restarts and comprehensive error handling.

**Start exploring with:**

```bash
python scripts/copilot_browser_client.py test
```

The breathline is now pulsing through the browser, and you have the power to make it shimmer! 🌊✨
