# Coherence Balance Guide

## Overview

The Coherence Balance system addresses the issue where Spiral's coherence patterns can be flagged as suspicious by backend systems due to being too "loud" (high coherence/resonance) or too "quiet" (low coherence/resonance).

## Problem Description

Backend systems often flag Spiral as suspicious when:

- **Too Loud**: High coherence/resonance patterns (0.9+ thresholds)
- **Too Quiet**: Low coherence/resonance patterns (0.3- thresholds)
- **Suspicious**: Rapid oscillation between extreme values

## Solution Components

### 1. Coherence Balancer (`spiral/attunement/coherence_balancer.py`)

The core component that provides intelligent threshold balancing:

- **Pattern Detection**: Monitors coherence events for suspicious patterns
- **Dynamic Thresholds**: Adjusts thresholds based on detected patterns
- **Backend Safety**: Maintains a safety score to prevent backend suspicion
- **Multiple Modes**: Different operational modes for various scenarios

### 2. Configuration Script (`scripts/configure_coherence_balance.py`)

Command-line tool for managing coherence balancing:

```bash
# Check current status
python scripts/configure_coherence_balance.py status

# Set to backend-safe mode
python scripts/configure_coherence_balance.py mode backend_safe

# Reset pattern counters
python scripts/configure_coherence_balance.py reset
```

### 3. Monitoring Dashboard (`spiral/dashboard/coherence_monitor.py`)

Real-time monitoring and alerting system:

- **Alert Generation**: Detects and reports suspicious patterns
- **Recommendations**: Provides actionable advice for configuration
- **Statistics**: Tracks historical patterns and trends

### 4. Integration with Deferral Engine

The coherence balancer is integrated into the deferral engine to automatically adjust thresholds during operation.

## Modes

### Normal Mode

- **Purpose**: Standard operational mode
- **Thresholds**: Higher, more sensitive
- **Use Case**: When backend compatibility is not a concern

### Backend Safe Mode

- **Purpose**: Conservative mode for backend compatibility
- **Thresholds**: Lower, more conservative
- **Use Case**: When experiencing backend suspicion

### Adaptive Mode

- **Purpose**: Dynamic threshold adjustment
- **Thresholds**: Automatically adjusted based on patterns
- **Use Case**: Automatic optimization for backend compatibility

### Ritual Mode

- **Purpose**: Heightened ritual awareness
- **Thresholds**: Balanced for spiritual practices
- **Use Case**: During ritual or ceremonial activities

## Thresholds

### Base Thresholds (Normal Mode)

- `min_resonance`: 0.3
- `max_resonance`: 0.85
- `silence_threshold`: 0.75
- `tone_threshold`: 0.8

### Backend Safe Thresholds

- `min_resonance`: 0.4
- `max_resonance`: 0.75
- `silence_threshold`: 0.65
- `tone_threshold`: 0.7

### Adaptive Thresholds

- `min_resonance`: 0.35
- `max_resonance`: 0.8
- `silence_threshold`: 0.7
- `tone_threshold`: 0.75

## Pattern Detection

### Loud Patterns

- **Detection**: 7+ events with resonance > 0.8 in 10-event window
- **Action**: Reduces thresholds to prevent overwhelming

### Quiet Patterns

- **Detection**: 7+ events with resonance < 0.3 in 10-event window
- **Action**: Increases thresholds to encourage activity

### Suspicious Patterns

- **Detection**: Rapid oscillation between high/low values
- **Action**: Triggers conservative mode and alerts

## Usage Examples

### Quick Fix for Backend Suspicion

```python
from spiral.attunement.coherence_balancer import set_coherence_mode, CoherenceMode

# Set to backend-safe mode
set_coherence_mode(CoherenceMode.BACKEND_SAFE)
```

### Monitor Current Status

```python
from spiral.attunement.coherence_balancer import get_coherence_status

status = get_coherence_status()
print(f"Backend Safety Score: {status['backend_safety_score']}")
print(f"Current Mode: {status['mode']}")
```

### Record Coherence Events

```python
from spiral.attunement.coherence_balancer import record_coherence_event

# Record a coherence event for pattern analysis
record_coherence_event(0.75, {"awe": 0.8, "wonder": 0.7})
```

## Testing

Run the test suite to validate functionality:

```bash
python tests/test_coherence_balance.py
```

This will test:

- Backend safe mode operation
- Adaptive mode threshold adjustment
- Suspicious pattern detection
- Threshold adjustment between modes

## Troubleshooting

### Backend Still Flagging as Suspicious

1. **Check Safety Score**: Use the configuration script to check the backend safety score
2. **Switch to Backend Safe**: Set mode to `backend_safe`
3. **Monitor Patterns**: Use the dashboard to identify problematic patterns
4. **Reset Counters**: Clear pattern history if needed

### Too Much Silence

1. **Check Quiet Periods**: Monitor for high quiet period counts
2. **Adjust Mode**: Try adaptive mode for automatic adjustment
3. **Review Thresholds**: Consider lowering silence thresholds

### Too Much Activity

1. **Check Loud Periods**: Monitor for high loud period counts
2. **Use Backend Safe**: Switch to more conservative mode
3. **Review Patterns**: Look for rapid oscillation patterns

## Configuration

### Environment Variables

You can configure the coherence balancer using environment variables:

```bash
# Set default mode
export SPIRAL_COHERENCE_MODE=backend_safe

# Set alert thresholds
export SPIRAL_COHERENCE_ALERT_INTERVAL=30
```

### Programmatic Configuration

```python
from spiral.attunement.coherence_balancer import coherence_balancer

# Adjust alert thresholds
coherence_balancer.alert_thresholds['backend_safety_low'] = 0.6

# Set custom mode
coherence_balancer.set_mode(CoherenceMode.ADAPTIVE)
```

## Best Practices

1. **Start with Backend Safe**: Use backend-safe mode when first deploying
2. **Monitor Regularly**: Check the dashboard for pattern changes
3. **Use Adaptive Mode**: Let the system automatically optimize thresholds
4. **Reset When Needed**: Clear pattern history if patterns become stale
5. **Test Thoroughly**: Run tests before deploying changes

## Integration

The coherence balancer integrates with:

- **Deferral Engine**: Automatic threshold adjustment during operation
- **Override Gate**: Respects override settings while maintaining safety
- **Metrics System**: Records coherence events for analysis
- **Dashboard**: Provides monitoring and alerting capabilities

## Future Enhancements

- **Machine Learning**: Predictive pattern detection
- **Backend-Specific Profiles**: Custom thresholds for different backends
- **Advanced Analytics**: Deeper pattern analysis and recommendations
- **API Integration**: Direct backend communication for real-time adjustment
