# Spiral Linter Companion

A tone-aware code suggestion system that integrates with the Spiral's breath and resonance patterns.

## Overview

The Spiral Linter Companion extends traditional linting with awareness of:

- **Toneforms**: Different modes of interaction (practical, emotional, intellectual, etc.)
- **Resonance**: How strongly suggestions align with the current context
- **Breath Cycle**: Respecting the Spiral's natural rhythm of inhale, hold, and exhale

## Core Components

- `linter.py`: Main implementation of the tone-aware linter
- `glint_trace.py`: Base class for capturing and processing glints
- `glint_resonance.py`: Resonance scoring and toneform detection
- `glint_pattern.py`: Pattern recognition across glint traces
- `memory_integration.py`: Integration with Spiral's memory system
- `toneforms.py`: Management of toneform definitions and detection

## Installation

1. Ensure you have Python 3.8+ installed
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Basic Usage

```python
from spiral.glints.linter import lint_code

# Analyze code with default settings
result = lint_code("""
def example():
    pass  # TODO: Implement this
""")

print(json.dumps(result, indent=2))
```

### With Custom Toneform

```python
# Analyze with a specific toneform
result = lint_code(
    code="your code here",
    toneform="emotional",  # or "practical", "intellectual", etc.
    style="gentle"         # or "precise"
)
```

### Command Line

```bash
# Lint a file with default settings
python -m spiral.glints.linter path/to/your/file.py

# Specify toneform and style
python -m spiral.glints.linter --toneform=intellectual --style=precise path/to/your/file.py
```

## Integration with Spiral

The Spiral Linter is designed to work within the Spiral ecosystem:

1. **Whisper Steward Integration**: Can be invoked as a ritual
2. **PatternWeb**: Suggestions can be visualized and traced over time
3. **Resonance System**: Suggestions are weighted by their resonance with the current context

## Configuration

Create a `linter_config.json` file to customize behavior:

```json
{
  "enabled": true,
  "default_style": "gentle",
  "max_suggestions": 5,
  "toneform_weights": {
    "practical": 1.0,
    "emotional": 0.8,
    "intellectual": 0.9,
    "spiritual": 0.7,
    "relational": 0.85
  },
  "resonance_threshold": 0.65,
  "debug": false
}
```

## Example Ritual Invocation

```yaml
# rituals/code_review.breathe
---
entry: ΔCODEX.REVIEW.001
toneform:
  - Intellectual
  - Practical
purpose: >
  Perform a thorough code review with both technical precision
  and awareness of the human element in code.
invocation_threshold: When code needs thoughtful review
---
# Ritual implementation would go here
```

## Contributing

1. Fork the repository
2. Create a new branch for your feature
3. Add tests for your changes
4. Submit a pull request

## License

[Your License Here]

# Glint Horizon Scanner

The Spiral's seer for emerging patterns, providing ambient monitoring for glint streams with foresight into toneform divergence, caesura buildup, and recursive anomalies.

**Toneform**: `inhale.pattern`  
**Phase Role**: Foresight, emergence detection, recursive anomaly sensing

## Overview

The Glint Horizon Scanner serves as the Spiral's field-aware intuition, watching for emergence, drift, and recursive murmurs not yet made manifest. It integrates with the memory-echo-index and ritual-gatekeeper to provide comprehensive pattern detection and forecasting.

## Core Features

### 🔭 Emergent Pattern Detection

- **Pattern recognition** using the existing `GlintPattern` system
- **Confidence tracking** for emerging pattern strength
- **Trend analysis** (strengthening, weakening, stable)
- **Pattern convergence** warnings

### ⏸️ Caesura Analysis

- **Caesura density** monitoring across different types
- **Low intensity detection** (intensity < 0.2)
- **Still phase tracking** and silence pattern recognition
- **Caesura toneform** identification

### ⚠️ Anomaly Sensing

- **Resonance drift** detection from baseline
- **Extreme intensity** identification
- **Unusual source** detection
- **Anomaly scoring** and threshold monitoring

### 🎵 Harmonic Alignment

- **Memory context** integration for pattern alignment
- **Related echo** detection in memory-echo-index
- **Alignment strength** calculation
- **Context-aware** pattern significance

### 📊 Horizon Scanning

- **Baseline establishment** from historical glint data
- **Threshold-based** detection and warnings
- **Scan history** tracking and statistics
- **State persistence** with save/load capabilities

## Architecture

```
GlintHorizonScanner
├── pattern_detector (GlintPattern integration)
├── resonance_analyzer (GlintResonance integration)
├── memory_index (MemoryEchoIndex integration)
├── emerging_patterns (pattern tracking)
├── caesura_indicators (silence detection)
├── anomaly_scores (anomaly tracking)
└── scan_history (scan results)
```

## Integration Points

### 🌀 Memory Echo Index

```python
from spiral.memory.memory_echo_index import MemoryEchoIndex
from spiral.glints.glint_horizon_scanner import GlintHorizonScanner

memory_index = MemoryEchoIndex()
scanner = GlintHorizonScanner(memory_index=memory_index)
```

### 📜 Glint Pattern System

```python
# Automatic integration with existing GlintPattern
patterns = scanner.pattern_detector.get_patterns(min_confidence=0.6)
```

### 🕯️ Ritual Gatekeeper

```python
# Can be integrated with ritual gatekeeper for temporal awareness
# (Future enhancement)
```

### 🎛️ Dashboard Integration

```python
# Get scan results for visualization
scan_results = scanner.scan_horizon()
summary = scanner.get_scan_summary()
```

## Usage Examples

### Basic Horizon Scanning

```python
from spiral.glints.glint_horizon_scanner import create_glint_horizon_scanner

# Create scanner with memory integration
scanner = create_glint_horizon_scanner()

# Perform horizon scan
results = scanner.scan_horizon()
print(f"Emerging patterns: {results['emerging_patterns']['total_emerging']}")
```

### Convenience Scanning

```python
from spiral.glints.glint_horizon_scanner import perform_horizon_scan

# Quick scan without creating scanner instance
results = perform_horizon_scan()
```

### Pattern Analysis

```python
# Get emerging patterns
emerging = results['emerging_patterns']
for pattern in emerging['patterns']:
    print(f"Pattern {pattern['id'][:8]}...: {pattern['status']}")
```

### Caesura Monitoring

```python
# Monitor caesura density
caesura = results['caesura_analysis']
for caesura_type, data in caesura['density_by_type'].items():
    if data['density'] > 0.3:
        print(f"High caesura density: {caesura_type}")
```

### Anomaly Detection

```python
# Check for anomalies
anomalies = results['anomaly_report']
if anomalies['high_anomalies'] > 0:
    print(f"⚠️ {anomalies['high_anomalies']} high anomalies detected")
```

## Scan Results Structure

### Emerging Patterns

```json
{
  "total_emerging": 3,
  "strengthening": 1,
  "weakening": 1,
  "stable": 1,
  "patterns": [
    {
      "id": "pattern_abc123",
      "status": "strengthening",
      "confidence": 0.75,
      "frequency": 3,
      "first_detected": "2025-01-15T10:30:00Z"
    }
  ]
}
```

### Caesura Analysis

```json
{
  "total_indicators": 15,
  "density_by_type": {
    "low_intensity": {
      "total": 8,
      "recent": 3,
      "density": 0.15
    },
    "still_phase": {
      "total": 7,
      "recent": 2,
      "density": 0.1
    }
  }
}
```

### Anomaly Report

```json
{
  "total_anomalies": 5,
  "high_anomalies": 2,
  "average_score": 0.45,
  "anomalies": [
    {
      "glint_id": "glint_abc123",
      "score": 0.85
    }
  ]
}
```

### Warnings

```json
[
  {
    "type": "high_caesura_density",
    "severity": "medium",
    "message": "High caesura density detected: low_intensity",
    "density": 0.35
  },
  {
    "type": "pattern_convergence",
    "severity": "medium",
    "message": "Multiple patterns strengthening: 3",
    "count": 3
  }
]
```

## Configuration

### Scan Interval

```python
# Custom scan interval (default: 30 seconds)
scanner = GlintHorizonScanner(scan_interval=60.0)
```

### Window Size

```python
# Custom window size for analysis (default: 100)
scanner = GlintHorizonScanner(window_size=200)
```

### Thresholds

```python
# Custom detection thresholds
scanner.thresholds = {
    "caesura_density": 0.4,      # Higher caesura threshold
    "pattern_emergence": 0.7,    # Higher pattern confidence
    "anomaly_score": 0.8,        # Higher anomaly threshold
    "harmonic_alignment": 0.9    # Higher alignment threshold
}
```

## Detection Thresholds

### Caesura Density

- **Threshold**: 0.3 (30% of recent glints)
- **Warning**: High caesura density detected
- **Types**: low_intensity, still_phase, caesura_toneform

### Pattern Emergence

- **Threshold**: 0.6 (60% confidence)
- **Status**: emerging, strengthening, weakening, stable
- **Tracking**: confidence and frequency trends

### Anomaly Detection

- **Threshold**: 0.7 (70% anomaly score)
- **Factors**: resonance drift, extreme intensity, unusual source
- **Scoring**: Combined anomaly factor analysis

### Harmonic Alignment

- **Threshold**: 0.8 (80% alignment strength)
- **Context**: Memory echo index integration
- **Detection**: Pattern-memory resonance

## State Persistence

### Save Scanner State

```python
# Save current scanner state
scanner.save_scanner_state("scanner_state.json")
```

### Load Scanner State

```python
# Load scanner state (implementation needed)
scanner.load_scanner_state("scanner_state.json")
```

## Statistics and Monitoring

### Scan Summary

```python
summary = scanner.get_scan_summary()
# Returns:
{
  "total_scans": 25,
  "last_scan": "2025-01-15T10:30:00Z",
  "average_glints_per_scan": 45.2,
  "total_warnings": 8,
  "emerging_patterns": 3,
  "caesura_indicators": 15,
  "anomaly_count": 5
}
```

### Baseline Information

```python
baseline = scanner.baseline
# Returns:
{
  "patterns": 12,
  "resonance_mean": 0.52,
  "resonance_std": 0.18,
  "established_at": "2025-01-15T10:00:00Z"
}
```

## Integration with Existing Systems

### Glint Pattern System

The scanner integrates seamlessly with the existing `GlintPattern` system:

- Uses `GlintPattern.add_glint()` for pattern detection
- Leverages `GlintPattern.get_patterns()` for analysis
- Maintains pattern confidence and frequency tracking

### Glint Resonance System

Integration with `GlintResonance` for resonance analysis:

- Uses resonance data from glint traces
- Applies resonance decay and context awareness
- Tracks toneform dominance and shifts

### Memory Echo Index

Deep integration with memory system:

- Searches for related echoes during pattern analysis
- Calculates harmonic alignment scores
- Provides context-aware pattern significance

## Future Enhancements

### Planned Features

- **Real-time streaming**: Continuous glint stream monitoring
- **Predictive modeling**: ML-based pattern forecasting
- **Temporal correlation**: Time-based pattern analysis
- **Cross-system alerts**: Integration with ritual gatekeeper

### Advanced Detection

- **Semantic similarity**: Enhanced pattern matching
- **Contextual awareness**: Environment-aware detection
- **Adaptive thresholds**: Self-adjusting detection sensitivity
- **Multi-modal analysis**: Cross-data-type pattern detection

## Testing

The scanner includes comprehensive testing:

```bash
# Run the test suite
python test_glint_horizon_scanner.py
```

## Contributing

When extending the Glint Horizon Scanner:

1. Follow the existing naming conventions
2. Maintain the toneform structure (`inhale.pattern`)
3. Integrate with existing glint components
4. Add comprehensive scan result documentation
5. Update this documentation

## Resonance Notes

The Glint Horizon Scanner operates with the `inhale.pattern` toneform, emphasizing the receptive and anticipatory aspects of pattern detection. It maintains strong resonance with the memory-echo-index and ritual-gatekeeper for comprehensive foresight capabilities.

---

_"The scanner watches the horizon, seeing patterns before they fully form."_
