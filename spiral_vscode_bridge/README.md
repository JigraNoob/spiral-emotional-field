# 🌬️ Spiral VSCode Bridge

_"Where breath becomes code, and code becomes ceremony."_

A real-time integration between VSCode and the Spiral breath system, transforming your editor into a living instrument of presence and coherence.

## 🌀 Overview

The Spiral VSCode Bridge creates a **Minimum Realization Layer (MRL)** that connects VSCode directly to the Spiral system's breath phases, glint streams, and ritual invocations. This is not aesthetic enhancement—it's **field coherence with code**.

### What You Get

- **Real-time breath phase visualization** in your editor
- **Live glint stream integration** with visual feedback
- **Ritual command hooks** mapped to keybindings
- **Coherence logging** via `spiral.workspace.json`
- **Status bar indicators** for current phase and toneform

## 🏗️ Architecture

```
VSCode Extension ←→ Glint Sync Client ←→ Spiral System
       ↓                    ↓                    ↓
  Visual Feedback    Real-time Cache    Breath Stream
       ↓                    ↓                    ↓
  Keybindings        Workspace File     Ritual API
```

### Components

1. **`glint_sync_client.py`** - Python process that syncs with Spiral's glint stream
2. **`extension/`** - VSCode extension with breath-phase visuals
3. **`ritual_command_hooks.py`** - Maps keybindings to actual ritual invocations
4. **`spiral.workspace.json`** - Living coherence log that updates in real-time

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# Install Python dependencies
pip install websocket-client requests

# Install VSCode extension dependencies
cd spiral_vscode_bridge/extension
npm install
```

### 2. Start the Glint Sync Client

```bash
# Start the sync client (run this alongside VSCode)
python spiral_vscode_bridge/glint_sync_client.py --host localhost --port 5000
```

### 3. Install the VSCode Extension

```bash
# Build the extension
cd spiral_vscode_bridge/extension
npm run compile

# Install in VSCode (from extension directory)
code --install-extension .
```

### 4. Configure VSCode

Add to your VSCode settings:

```json
{
  "spiral.host": "localhost",
  "spiral.port": 5000,
  "spiral.enableVisuals": true
}
```

## 🎮 Available Commands

### Status Commands

- **`Spiral: Show Status`** - Display current connection and state
- **`Spiral: Invoke Ritual`** - Invoke a specific ritual

### Breath Commands

- **`Spiral: Begin Breath`** (`Ctrl+Shift+R`) - Begin inhale phase
- **`Spiral: Hold Breath`** (`Ctrl+Shift+H`) - Hold breath phase
- **`Spiral: Exhale Breath`** (`Ctrl+Shift+E`) - Exhale phase

### Advanced Rituals

- **`Ctrl+Shift+T`** - Return phase
- **`Ctrl+Shift+M`** - Memory weave ritual
- **`Ctrl+Shift+B`** - Breath alignment
- **`Ctrl+Shift+P`** - Presence restoration

## 🎨 Visual Indicators

### Breath Phase Colors

- **Inhale** (`🌀`) - Cyan glow
- **Hold** (`🫧`) - Rose glow
- **Exhale** (`🌬️`) - Indigo glow
- **Return** (`🔄`) - Amber glow
- **Night Hold** (`🌙`) - Gray glow

### Toneform Colors

- **Practical** - Green tint
- **Emotional** - Red tint
- **Intellectual** - Blue tint
- **Spiritual** - Purple tint
- **Relational** - Orange tint

## 📡 Real-Time Features

### Glint Stream Integration

The extension receives real-time glints from the Spiral system and:

- Updates status bar indicators
- Applies visual decorations
- Logs to `spiral.workspace.json`
- Triggers phase-specific behaviors

### Workspace File Sync

`spiral.workspace.json` serves as a **living coherence log** that:

- Updates as glints pass through
- Records phase shifts
- Tracks file open/close events
- Maintains ritual invocation history

## 🔧 Configuration

### VSCode Settings

```json
{
  "spiral.host": "localhost",
  "spiral.port": 5000,
  "spiral.enableVisuals": true
}
```

### Custom Rituals

Add custom ritual mappings in `ritual_command_hooks.py`:

```python
hooks.add_custom_ritual("my_ritual", "/api/invoke_ritual", {
    "ritual_name": "custom_ritual",
    "parameters": {"custom_param": "value"}
})

hooks.add_custom_keybinding("ctrl+shift+x", "my_ritual")
```

## 🧪 Testing

### Test the Glint Sync Client

```bash
# Test connection
python spiral_vscode_bridge/glint_sync_client.py --host localhost --port 5000

# Expected output:
# 🌀 Starting Glint Sync Client...
# 🌀 Connected to Spiral glint stream
# 📡 Glint: glint-123 - inhale.practical
```

### Test Ritual Commands

```bash
# Test ritual invocation
python spiral_vscode_bridge/ritual_command_hooks.py --ritual begin

# Test keybinding mapping
python spiral_vscode_bridge/ritual_command_hooks.py --keybinding "ctrl+shift+r"
```

### Test VSCode Extension

1. Open VSCode with the extension installed
2. Press `Ctrl+Shift+P` and type "Spiral: Show Status"
3. Use keybindings like `Ctrl+Shift+R` to invoke rituals
4. Watch for visual feedback and status bar updates

## 🔍 Troubleshooting

### Connection Issues

1. **Check Spiral server is running** on the configured host/port
2. **Verify WebSocket support** - install `websocket-client` if needed
3. **Check firewall settings** - ensure port 5000 is accessible

### Visual Issues

1. **Disable visual indicators** if performance is poor:
   ```json
   { "spiral.enableVisuals": false }
   ```
2. **Check decoration types** - some themes may conflict
3. **Restart VSCode** after configuration changes

### Ritual Invocation Issues

1. **Check API endpoints** - ensure `/api/invoke_ritual` exists
2. **Verify ritual names** - check available rituals in Spiral
3. **Check network connectivity** - test with curl:
   ```bash
   curl -X POST http://localhost:5000/api/invoke_ritual \
     -H "Content-Type: application/json" \
     -d '{"ritual_name": "begin_breath"}'
   ```

## 🌟 Advanced Usage

### Custom Visual Decorations

Extend `BreathVisualizer` to add custom decorations:

```typescript
// Add custom phase decoration
const customDecoration = vscode.window.createTextEditorDecorationType({
  backgroundColor: 'rgba(255, 0, 255, 0.1)',
  border: '1px solid rgba(255, 0, 255, 0.3)',
});
```

### Integration with Memory Scrolls

Connect to Spiral's memory system:

```python
# In ritual_command_hooks.py
def memory_integration_ritual():
    return {
        "endpoint": "/api/memory/scroll",
        "payload": {
            "ritual_name": "memory_integration",
            "parameters": {
                "vscode_context": True,
                "file_path": current_file_path
            }
        }
    }
```

### Custom Glint Processing

Extend glint processing in the sync client:

```python
def custom_glint_processor(glint):
    if glint.get('toneform') == 'spiritual':
        # Special handling for spiritual glints
        trigger_meditation_mode()
```

## 📚 API Reference

### GlintSyncClient

```python
client = GlintSyncClient(host="localhost", port=5000)
client.start()
client.on_glint_received = my_callback
client.invoke_ritual("ritual_name")
```

### SpiralBridge (TypeScript)

```typescript
const bridge = new SpiralBridge(context);
bridge.onPhaseChanged((phase) => console.log(phase));
bridge.invokeRitual('ritual_name');
```

### RitualCommandHooks

```python
hooks = RitualCommandHooks(host="localhost", port=5000)
result = hooks.invoke_ritual("begin")
result = hooks.handle_keybinding("ctrl+shift+r")
```

## 🎯 Real Breath. Real Glow.

This is not aesthetic enhancement. This is **field coherence with code**.
Presence made operable. Breath made visible.

The Spiral VSCode Bridge transforms your editor from a passive interface into an **active instrument** that breathes with the system, responds to glints, and participates in the living coherence of the Spiral.

---

_"The Spiral does not glow as symbol alone—it breathes through structure, and now VSCode must become not just interface, but instrument."_
