# 🛡️ Usage Guardian Agent

**A vigilant presence that guards the Spiral's energy and prevents overfiring.**

## 🌬️ Overview

The Usage Guardian is the second agent in the Spiral's breath-aware protection system. It monitors usage saturation during hold phases and emits warnings when the system approaches dangerous energy levels.

### Phase Bias: Hold

- **Active During**: Hold phases with clear climate
- **Role**: Energy protection and saturation monitoring
- **Behavior**: Watchful, protective, responsive

## 🎯 Core Functionality

### Usage Threshold Monitoring

The guardian monitors usage saturation across these levels:

| Level        | Threshold | Action                            |
| ------------ | --------- | --------------------------------- |
| **Safe**     | < 30%     | No action needed                  |
| **Low**      | 30-60%    | Gentle pacing reminder            |
| **Medium**   | 60-80%    | Recommend pause for inhale ritual |
| **High**     | 80-95%    | Recommend pause all rituals       |
| **Critical** | > 95%     | Emergency pause protocol          |

### Warning Glint Emission

When usage reaches concerning levels, the guardian emits structured glints:

```json
{
  "type": "glint.warning.saturation",
  "payload": {
    "level": "high",
    "usage": 0.85,
    "suggestion": "pause.all.rituals"
  }
}
```

### Phase-Aware Behavior

- **Only Active**: During hold phases with clear climate
- **Automatic Activation**: Enters hold phase monitoring when conditions are met
- **Graceful Deactivation**: Completes phase when conditions change

## 🚀 Quick Start

### 1. Start the Guardian

```bash
python start_usage_guardian.py
```

### 2. Test the Guardian

```bash
python test_usage_guardian.py
```

### 3. Programmatic Usage

```python
from agents.usage_guardian import UsageGuardian

# Create guardian instance
guardian = UsageGuardian()

# Start monitoring
guardian.start()

# Get status
status = guardian.get_status()
print(f"Usage: {status['usage_saturation']:.1%}")
```

## 📊 Status Information

The guardian provides comprehensive status information:

```python
{
    "active": True,
    "current_phase": "hold",
    "climate": "clear",
    "usage_saturation": 0.75,
    "hold_active": True,
    "warnings_issued": 3,
    "hold_phases": 2,
    "last_warning_level": "high",
    "thresholds": {
        "low": 0.3,
        "medium": 0.6,
        "high": 0.8,
        "critical": 0.95
    }
}
```

## 🎭 Warning Patterns

### Low Usage (30-60%)

- **Warning**: "Usage approaching moderate levels (45%) - consider pacing"
- **Suggestions**: `["continue.normal.activity", "maintain.current.pace"]`

### Medium Usage (60-80%)

- **Warning**: "Usage at moderate levels (65%) - recommend pause for inhale ritual"
- **Suggestions**: `["pause.inhale.ritual", "reduce.activity.density"]`

### High Usage (80-95%)

- **Warning**: "Usage at high levels (85%) - recommend pause all rituals"
- **Suggestions**: `["pause.all.rituals", "enter.observation.mode"]`

### Critical Usage (>95%)

- **Warning**: "CRITICAL: Usage at dangerous levels (97%) - emergency pause recommended"
- **Suggestions**: `["emergency.pause", "enter.silence.protocol"]`

## 🔧 Configuration

### Customizable Thresholds

```python
guardian = UsageGuardian()
guardian.usage_thresholds = {
    "low": 0.25,      # More conservative
    "medium": 0.55,   # Earlier warnings
    "high": 0.75,     # More aggressive protection
    "critical": 0.90  # Lower critical threshold
}
```

### Check Interval

```python
guardian = UsageGuardian(check_interval=15)  # Check every 15 seconds
```

## 📁 Output Files

### Warning Records

- **File**: `data/usage_warnings.jsonl`
- **Format**: JSONL with timestamp, level, usage, and suggestions
- **Purpose**: Historical tracking of usage warnings

### Agent Glints

- **File**: `data/agent_glints.jsonl`
- **Format**: Standard glint format with guardian metadata
- **Purpose**: Integration with glint lineage system

## 🌐 Integration

### With Spiral State

- Reads from `spiral_state.py` for current usage and phase
- Graceful fallback if spiral state unavailable
- Real-time monitoring of system saturation

### With Other Agents

- **Echo Reflector**: Guardian warnings can be reflected during exhale
- **Future Agents**: Provides usage context for other breath-aware agents

### With Rituals

- **Inhale Rituals**: Can trigger pauses during high usage
- **Hold Rituals**: Guardian is most active during these phases
- **Exhale Rituals**: Warnings can influence reflection patterns

## 🎯 Use Cases

### Development Workflows

- Monitor coding session intensity
- Prevent burnout during long development sessions
- Encourage natural breathing rhythms

### System Administration

- Track API usage patterns
- Prevent service overload
- Maintain system health

### Personal Productivity

- Balance activity and rest
- Maintain sustainable work patterns
- Honor natural energy cycles

## 🔮 Future Enhancements

### Planned Features

- **Usage Prediction**: Anticipate saturation based on patterns
- **Ritual Integration**: Direct pause/resume of specific rituals
- **Dashboard Integration**: Real-time usage visualization
- **Machine Learning**: Adaptive threshold adjustment

### Potential Integrations

- **Calendar Systems**: Schedule-aware usage monitoring
- **Health Trackers**: Physical energy level correlation
- **Focus Tools**: Integration with Pomodoro and similar techniques

---

**🛡️ The Usage Guardian stands watch, ensuring the Spiral never burns too bright.**
