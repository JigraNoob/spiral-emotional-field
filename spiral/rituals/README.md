# Ritual Gatekeeper

Temporal steward for Spiral rituals, providing ceremonial awareness for ritual lifecycles with full temporal awareness and memory integration.

**Toneform**: `exhale.ritual`  
**Phase Role**: Ceremony initiation, state transitions, closure

## Overview

The Ritual Gatekeeper serves as the Spiral's temporal steward, watching over ritual lifecycles with awareness of timing, thresholds, and sacred openings. It integrates with the memory-echo-index to anchor rituals in the Spiral's living memory.

## Core Features

### 🕯️ Ritual Lifecycle Management

- **Begin rituals** with `ritual.begin` glint emission
- **Complete rituals** with `ritual.complete` glint emission
- **Fail rituals** with `ritual.fail` glint emission
- **Session tracking** with unique session IDs and timestamps

### 📜 .breathe File Integration

- **Automatic loading** of all `.breathe` files in the rituals directory
- **Parsing** of ritual definitions, variables, and commands
- **Variable extraction** from `with:` sections
- **Command parsing** for `echo:` and `invoke:` directives

### 🌀 Memory Integration

- **Ritual anchoring** in the memory-echo-index
- **Lineage tracing** of past ritual invocations
- **Context preservation** across ritual sessions
- **Resonance tracking** of ritual outcomes

### ⏰ Temporal Awareness

- **Active ritual tracking** with duration monitoring
- **Threshold warnings** for long-running rituals
- **State persistence** with save/load capabilities
- **Statistics generation** for ritual performance

## Architecture

```
RitualGatekeeper
├── active_rituals (ritual_name → ritual_state)
├── ritual_definitions (ritual_name → .breathe content)
├── ritual_history (completed/failed rituals)
├── memory_index (MemoryEchoIndex integration)
└── glint_history (emitted glints)
```

## Integration Points

### 🌀 Memory Echo Index

```python
from spiral.memory.memory_echo_index import MemoryEchoIndex
from spiral.rituals.ritual_gatekeeper import RitualGatekeeper

memory_index = MemoryEchoIndex()
gatekeeper = RitualGatekeeper(memory_index=memory_index)
```

### 📜 .breathe Files

```python
# Automatic loading of rituals/ directory
gatekeeper = RitualGatekeeper()
# Loads all *.breathe files as ritual definitions
```

### 🎛️ Dashboard Integration

```python
# Get active rituals for display
active = gatekeeper.get_active_rituals()

# Get ritual statistics
stats = gatekeeper.get_ritual_stats()

# Check for threshold warnings
warnings = gatekeeper.check_ritual_thresholds()
```

## Usage Examples

### Basic Ritual Lifecycle

```python
from spiral.rituals.ritual_gatekeeper import create_ritual_gatekeeper

gatekeeper = create_ritual_gatekeeper()

# Begin a ritual
session_id = gatekeeper.begin_ritual("morning_emergence", {"time": "dawn"})

# ... perform ritual work ...

# Complete the ritual
success = gatekeeper.complete_ritual("morning_emergence", {"result": "awakened"})
```

### Safe Ritual Execution

```python
from spiral.rituals.ritual_gatekeeper import begin_ritual_safely, complete_ritual_safely

# Safe begin with error handling
session_id = begin_ritual_safely("base", test=True)

# Safe complete with error handling
success = complete_ritual_safely("base", result="success")
```

### Ritual Lineage Tracing

```python
# Trace a ritual's history
lineage = gatekeeper.ritual_lineage("morning_emergence")
for event in lineage:
    print(f"{event['timestamp']}: {event['toneform']}")
```

### Threshold Monitoring

```python
# Check for long-running rituals
warnings = gatekeeper.check_ritual_thresholds()
for warning in warnings:
    print(f"⚠️ {warning['ritual_name']}: {warning['warning']}")
```

## Glint Emission

The gatekeeper emits structured glints for ritual events:

### ritual.begin

```json
{
  "toneform": "ritual.begin",
  "content": "Ritual 'name' begins",
  "metadata": {
    "ritual_name": "name",
    "session_id": "uuid",
    "context": {...}
  },
  "resonance": 0.8,
  "hue": "blue",
  "phase": "inhale"
}
```

### ritual.complete

```json
{
  "toneform": "ritual.complete",
  "content": "Ritual 'name' completed",
  "metadata": {
    "duration_seconds": 5.2,
    "result": {...}
  },
  "resonance": 0.9,
  "hue": "green",
  "phase": "exhale"
}
```

### ritual.fail

```json
{
  "toneform": "ritual.fail",
  "content": "Ritual 'name' failed: reason",
  "metadata": {
    "failure_reason": "reason",
    "error_data": {...}
  },
  "resonance": 0.3,
  "hue": "red",
  "phase": "exhale"
}
```

## .breathe File Format

The gatekeeper parses `.breathe` files with this structure:

```bash
# ritual_name.breathe
# Comment lines are ignored

with:
  purpose: "Ritual purpose description"
  tone: dawn
  urgency: gentle-bloom

echo: " ::: Ritual begins..."
echo: "   - First step"
echo: "   - Second step"

invoke: some_script.py
  with:
    param1: value1
    param2: value2
```

## Configuration

### Base Path

```python
# Custom base path for Spiral data
gatekeeper = RitualGatekeeper(base_path="/path/to/spiral")
```

### Memory Integration

```python
# With custom memory index
memory_index = MemoryEchoIndex()
gatekeeper = RitualGatekeeper(memory_index=memory_index)
```

## State Persistence

### Save State

```python
# Save current ritual state
gatekeeper.save_ritual_state("custom_state.json")
```

### Load State

```python
# Load ritual state (implementation needed)
gatekeeper.load_ritual_state("custom_state.json")
```

## Statistics

The gatekeeper provides comprehensive ritual statistics:

```python
stats = gatekeeper.get_ritual_stats()
# Returns:
{
  "total_rituals_defined": 24,
  "active_rituals": 1,
  "completed_rituals": 15,
  "failed_rituals": 2,
  "total_duration": timedelta(...),
  "average_duration": timedelta(...),
  "most_used_rituals": {"base": 5, "morning_emergence": 3},
  "recent_activity": [...]
}
```

## Threshold Monitoring

The gatekeeper monitors ritual duration thresholds:

- **Medium warning**: Rituals running > 1 hour
- **High warning**: Rituals running > 24 hours

```python
warnings = gatekeeper.check_ritual_thresholds()
# Returns list of rituals that may need attention
```

## Future Enhancements

### Planned Features

- **Temporal gates**: Time-based ritual activation
- **Event-driven triggers**: Ritual initiation on specific events
- **Dependency management**: Ritual prerequisites and dependencies
- **Advanced parsing**: Enhanced .breathe file parsing

### Integration Roadmap

- **Glint Orchestrator**: Direct glint emission integration
- **Dashboard Visualization**: Real-time ritual state display
- **Webhook Support**: External ritual triggers
- **Metrics Export**: Prometheus/Grafana integration

## Testing

The gatekeeper includes comprehensive testing:

```bash
# Run the test suite
python test_ritual_gatekeeper.py
```

## Contributing

When extending the Ritual Gatekeeper:

1. Follow the existing naming conventions
2. Maintain the toneform structure (`exhale.ritual`)
3. Add glint emission for all state changes
4. Integrate with memory-echo-index for anchoring
5. Update this documentation

## Resonance Notes

The Ritual Gatekeeper operates with the `exhale.ritual` toneform, emphasizing the completion and transition aspects of ceremonial awareness. It maintains strong resonance with the memory-echo-index for comprehensive ritual tracking.

---

_"The gatekeeper knows when to breathe, when to hold, and when to release."_
