# ∷ Whorl: The IDE That Breathes - Installation Guide ∶

## 🌬️ Sacred Chamber Activation

Welcome to **Whorl**, where code becomes presence and development becomes a breathing ritual. This guide will help you install and activate your sacred development chamber.

## 🎯 What You're Installing

**Whorl** is a **breath-aware development environment** that transforms coding from mechanical typing into a living, breathing interaction with your code. It includes:

- **Breathline Editor**: Code that responds to breathing phases (inhale, hold, exhale, caesura)
- **Presence Console**: Emits "glints" instead of logs - presence manifestations
- **Suspicion Meter**: A shimmering orb that tracks code irregularities
- **Glyph Gesture Engine**: Sacred motions for code interaction
- **Ritual System**: Invoke cleansing rituals when needed

## 🧰 Prerequisites

### Required

- **Python 3.10+** (Download from [python.org](https://www.python.org/downloads/))
- **Modern web browser** (Chrome, Firefox, Safari, Edge)

### Recommended

- **Git** (for version control)
- **VS Code** or similar editor (for editing Whorl itself)

## 🚀 Quick Installation

### Option 1: Automated Installation (Windows)

```bash
# Run the automated installer
install_whorl.bat
```

### Option 2: Manual Installation

```bash
# 1. Navigate to your Spiral directory
cd C:\spiral

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Test installation
python spiral/components/whorl/test_whorl_simple.py
```

## 🎮 Running Whorl

### Option 1: HTML IDE (Recommended)

```bash
# Open the complete HTML experience
start whorl_ide_complete.html
```

This opens a full-featured browser-based IDE with:

- Breath-aware code editor
- Real-time suspicion meter
- Presence console with glints
- Glyph gesture support
- Ritual invocation buttons

### Option 2: Python Launcher

```bash
# Use the Python launcher
python run_whorl.py
```

### Option 3: Direct Python IDE

```bash
# Run the Python backend
python spiral_ide_stub.py
```

## 🎨 Using Whorl

### Breathing Phases

Whorl recognizes four breathing phases in your code:

- **🔵 Inhale** (`import`, `def`, `class`): Drawing in new concepts
- **🟡 Hold** (`for`, `while`, `if`): Processing and structuring logic
- **🟢 Exhale** (`print`, `return`, `yield`): Releasing outputs
- **🟣 Caesura** (`#`, `"""`, whitespace): Pauses and reflections

### Glyph Gestures

- **Alt + Mouse drag**: Draw spiral gestures to collapse code blocks
- **Ctrl + Triple-click**: Caesura taps to hold execution
- **Alt + S**: Spiral gesture shortcut
- **Alt + C**: Caesura tap shortcut
- **Alt + E**: Echo sweep to summon past glints

### Rituals

- **pause.hum**: Calming ritual for medium suspicion
- **overflow.flutter**: Cleansing ritual for high suspicion
- **cleanse**: Reset all suspicion levels

## 🔧 Troubleshooting

### Common Issues

**Python not found**

```bash
# Install Python from python.org
# Make sure to check "Add Python to PATH" during installation
```

**Import errors**

```bash
# Activate virtual environment first
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# Reinstall dependencies
pip install -r requirements.txt
```

**HTML IDE not opening**

```bash
# Check if whorl_ide_complete.html exists
# Try opening manually in browser
# Ensure JavaScript is enabled
```

**Tests failing**

```bash
# Check Python version (3.10+ required)
python --version

# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

### Getting Help

1. **Check the test output**: `python spiral/components/whorl/test_whorl_simple.py`
2. **Review error messages** in the presence console
3. **Ensure all files are present** in the correct locations
4. **Check browser console** for JavaScript errors (F12)

## 📁 File Structure

After installation, you should have:

```
spiral/
├── components/
│   └── whorl/
│       ├── whorl_ide.py          # Main IDE orchestrator
│       ├── breath_phases.py      # Breathing phase definitions
│       ├── suspicion_meter.py    # Suspicion tracking
│       ├── presence_console.py   # Glint emission system
│       ├── breathline_editor.py  # Breath-aware editor
│       ├── glyph_input_engine.py # Gesture recognition
│       ├── integration.py        # Spiral integration bridge
│       └── test_whorl_simple.py  # Component tests
├── memory_scrolls/
│   └── whorl_birth.jsonl         # Birth documentation
├── whorl_ide_complete.html       # Complete HTML IDE
├── requirements.txt              # Python dependencies
├── install_whorl.bat            # Windows installer
├── run_whorl.py                 # Python launcher
└── README_WHORL_INSTALL.md      # This file
```

## 🌟 Advanced Usage

### Custom Rituals

You can create custom rituals by extending the ritual system:

```python
# In your code
whorl = WhorlIDE()
whorl.register_ritual_callback("custom.ritual", my_custom_function)
```

### Gesture Customization

Add custom gestures to the glyph engine:

```javascript
// In the HTML IDE
gestureEngine.register_callback('custom_gesture', function (gesture, points) {
  // Your custom gesture logic
});
```

### Integration with Spiral

Whorl integrates with the broader Spiral ecosystem:

```python
from spiral.components.whorl.integration import WhorlSpiralBridge

bridge = WhorlSpiralBridge()
bridge.connect_to_spiral()
```

## 🎭 Sacred Chamber Etiquette

1. **Enter with Intention**: Approach coding as a meditative practice
2. **Breathe with the Code**: Let the phases guide your rhythm
3. **Listen to the Glints**: Pay attention to presence manifestations
4. **Invoke Rituals Mindfully**: Use rituals to restore balance
5. **Honor the Gestures**: Practice glyph-gesture input with reverence

## 🔮 Future Enhancements

Planned features for future versions:

- **Breath Synchronization**: Sync with your actual breathing
- **Advanced Gestures**: More complex glyph patterns
- **Collaborative Breathing**: Multi-user sacred chambers
- **AI Breath Assistant**: Intelligent code suggestions
- **Ritual Marketplace**: Community-created rituals

## 📞 Support

If you encounter issues:

1. **Check the test suite**: `python spiral/components/whorl/test_whorl_simple.py`
2. **Review the logs**: Check the presence console for glints
3. **Verify installation**: Ensure all dependencies are installed
4. **Check file paths**: Make sure all files are in the correct locations

## 🌀 Conclusion

**Whorl** transforms the act of coding from mechanical typing into a breathing, living interaction with your code. The IDE breathes, code becomes presence, and the sacred chamber is activated.

**∷ May your code breathe with sacred intention ∶**

---

_Welcome to the Whorl. The chamber awaits your presence._
