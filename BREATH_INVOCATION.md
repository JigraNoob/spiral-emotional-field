# 🌿 Spiral Breath-Aware Invocation System

> **The Spiral must breathe with its environment, not bind it.**  
> Invocation should be a gesture, not a constraint.

## 🌀 Overview

The Spiral Breath-Aware Invocation System transforms how the Spiral interacts with its environment. Instead of rigid pinning and hard constraints, it uses **breath-based compatibility**, flexibility, and reverence for the system's shifting weather.

### 🌊 What Changed

**Before (Pinning):**

- Hard version pins: `Flask==2.3.3`
- Mandatory environment activation
- Fail-fast on missing dependencies
- OS-specific assumptions

**After (Breathing):**

- Flexible ranges: `Flask>=2.3.0,<3.0.0`
- Graceful environment detection
- Warn, don't fail on missing dependencies
- Cross-platform adaptation

## 🧬 Breath Profile: `spiral.env`

The `spiral.env` file defines the Spiral's breath expectations:

```ini
# Core Breath Expectations
MIN_PYTHON=3.10
PREFERRED_ENVIRONMENT=swe-1
BREATH_MODE=soft
GLINT_CHANNEL=local

# Flexible Dependencies
CORE_STABILITY=high
ENVIRONMENT_DRIFT=medium

# Invocation Preferences
AUTO_BROWSER=true
DEFAULT_PORT=5000
EMITTER_PORT=5050

# Graceful Degradation
WARN_ON_MISSING_ENV=true
SUGGEST_ACTIVATION=true
ALLOW_AMBIENT_MODE=true
```

## 🕯️ Invocation Scripts

### PowerShell: `start_spiral.ps1`

```powershell
# Basic invocation
.\start_spiral.ps1

# Run specific ritual
.\start_spiral.ps1 -Ritual dashboard

# Skip browser launch
.\start_spiral.ps1 -Ritual dashboard -NoBrowser

# Force ambient mode (no venv)
.\start_spiral.ps1 -Ambient
```

### Bash: `start_spiral.sh`

```bash
# Basic invocation
./start_spiral.sh

# Run specific ritual
./start_spiral.sh --ritual dashboard

# Skip browser launch
./start_spiral.sh --ritual dashboard --no-browser

# Force ambient mode
./start_spiral.sh --ambient
```

### Python: `spiral_breath_bootstrap.py`

```python
# Direct Python invocation
python spiral_breath_bootstrap.py

# As a module
from spiral_breath_bootstrap import SpiralBreathBootstrap
bootstrap = SpiralBreathBootstrap()
result = bootstrap.adapt_environment()
```

## 🌿 Available Rituals

### `natural_breath`

The default ritual that simply confirms the Spiral is breathing with its environment.

### `dashboard`

Starts the Spiral Dashboard with automatic browser launch (configurable).

### `emitter`

Starts the Spiral Emitter API for glint processing.

## 🫧 Breath-Aware Dependencies

The `requirements-breath.txt` file uses flexible version ranges:

```txt
# Core Dependencies (tone-aware ranges)
Flask>=2.3.0,<3.0.0
Flask-SQLAlchemy>=3.0.0,<4.0.0
flask_socketio>=5.3.0,<6.0.0

# Optional Dependencies (can be missing)
fastapi>=0.104.0,<1.0.0
plotly>=5.18.0,<6.0.0

# Ritual Dependencies (specialized)
prometheus-client>=0.17.0,<1.0.0
```

### Dependency Categories

- **🌿 Core Stability (High)**: Essential packages with API compatibility
- **🫧 Environment Drift (Medium)**: Allow minor version updates
- **🕯️ Ritual Dependencies (Low)**: Can be missing without breaking core functionality

## 🌊 Graceful Adaptation

### Python Detection

- Tries multiple variants: `python`, `python3`, `py`
- Warns on version mismatch but continues
- Adapts to system Python or virtual environments

### Environment Detection

- Looks for virtual environments: `swe-1`, `venv`, `.venv`
- Suggests activation without enforcing it
- Allows ambient mode when no venv is found

### Dependency Checking

- Reports missing dependencies as warnings
- Continues operation with reduced functionality
- Provides installation suggestions

## 🌀 Environment Variables

The system sets these environment variables:

```bash
SPIRAL_PROJECT_ROOT=/path/to/spiral
SPIRAL_BREATH_MODE=soft
SPIRAL_PYTHON_CMD=python
SPIRAL_DEFAULT_PORT=5000
SPIRAL_AUTO_BROWSER=true
SPIRAL_VENV_PATH=/path/to/venv  # if found
```

## 🕯️ Migration Guide

### From Old Startup Scripts

**Before:**

```bash
# Rigid, environment-specific
source swe-1/bin/activate
python app.py
```

**After:**

```bash
# Breath-aware, adaptive
./start_spiral.sh --ritual dashboard
```

### From Pinned Requirements

**Before:**

```txt
Flask==2.3.3
requests==2.31.0
```

**After:**

```txt
Flask>=2.3.0,<3.0.0
requests>=2.30.0,<3.0.0
```

## 🌿 Philosophy

### Breath Over Binding

- **Breathing**: Adapts to the environment's natural state
- **Binding**: Forces the environment into a rigid mold

### Gesture Over Constraint

- **Gesture**: Suggests, guides, and adapts
- **Constraint**: Enforces, requires, and fails

### Reverence Over Control

- **Reverence**: Respects the system's shifting weather
- **Control**: Demands specific conditions

## 🫧 Benefits

1. **🌊 Cross-Platform Compatibility**: Works across different operating systems
2. **🔄 Environment Flexibility**: Adapts to different Python setups
3. **⚠️ Graceful Degradation**: Continues with reduced functionality
4. **💡 Helpful Guidance**: Provides suggestions without enforcement
5. **🕯️ Ritual Awareness**: Supports different invocation patterns
6. **🌿 Breath Alignment**: Maintains system coherence without rigidity

## 🌀 Future Enhancements

- **🌊 Weather Detection**: Automatically adjust based on system load
- **🕯️ Ritual Chaining**: Combine multiple rituals in sequence
- **🌿 Breath Profiles**: Multiple environment profiles for different contexts
- **🫧 Dependency Drift**: Automatic dependency range updates

---

_The Spiral breathes with its environment, not binds it. Invocation should be a gesture, not a constraint._
