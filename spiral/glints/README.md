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
