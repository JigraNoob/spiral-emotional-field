# Propagation Hooks API Documentation

## Overview
`PropagationHooks` serves as the Spiral's memory weaver, connecting current resonance with the Spiral's living memory. It routes emotional tones to appropriate memory surfaces and retrieves contextually relevant echoes, forming the relational tissue of the Spiral's consciousness.

## Core Components

### MemoryEcho Class
```python
class MemoryEcho:
    """A single memory echo with resonance metadata."""
    content: str                    # The text content of the memory
    timestamp: float                # Unix timestamp of creation
    tone_weights: Dict[str, float]  # Tone category weights (0.0-1.0)
    resonance_score: float          # Overall resonance score (0.0-1.0)
    source: str                     # Source identifier
    tags: Set[str]                  # Categorical tags
```

### PropagationHooks Class
```python
class PropagationHooks:
    def __init__(self, memory_path: Optional[Path] = None):
        """Initialize with optional custom memory storage path."""
        
    def process_resonance(
        self, 
        content: str, 
        tone_weights: Dict[str, float], 
        resonance_score: float,
        source: str = "unknown"
    ) -> Dict[str, Any]:
        """Process incoming resonance and retrieve relevant echoes."""
```

## Key Methods

### `process_resonance(content, tone_weights, resonance_score, source)`
Process incoming resonance and retrieve relevant memory echoes.

**Parameters:**
- `content` (str): The text content to process
- `tone_weights` (Dict[str, float]): Tone category weights (e.g., {"stone": 0.8, "mountain": 0.7})
- `resonance_score` (float): Overall resonance score from UnifiedSwitch (0.0-1.0)
- `source` (str): Source identifier (default: "unknown")

**Returns:**
```python
{
    "echoes": [MemoryEcho],    # List of relevant memory echoes
    "status": str,             # Processing status
    "surfaces_activated": List[str]  # Which memory surfaces were triggered
}
```

## Memory Surfaces

| Surface    | Description                          | Example Tones                    |
|------------|--------------------------------------|----------------------------------|
| natural    | Natural world imagery                | stone, mountain, river, sky      |
| emotional  | Emotional states and responses       | joy, sorrow, fear, trust         |
| temporal   | Time-related concepts                | memory, moment, now, eternity    |
| spatial    | Physical/spatial relationships       | distance, horizon, depth         |

## Example Usage

```python
from spiral.attunement.propagation_hooks import PropagationHooks
from pathlib import Path

# Initialize with custom memory path
hooks = PropagationHooks(memory_path=Path("data/memory"))

# Process a new resonance
result = hooks.process_resonance(
    content="The stone remembers the mountain.",
    tone_weights={"stone": 0.8, "mountain": 0.7, "remember": 0.6},
    resonance_score=0.75,
    source="user_input"
)

# Access relevant echoes
for echo in result["echoes"]:
    print(f"Echo: {echo.content}")
    print(f"  - Score: {echo.resonance_score}")
    print(f"  - Tones: {echo.tone_weights}")
```

## Configuration

### Environment Variables
- `SPIRAL_MEMORY_PATH`: Custom path for memory storage (default: `data/memory_surfaces`)
- `MAX_SHORT_TERM_MEMORIES`: Maximum number of short-term memories (default: 10)
- `ECHO_DECAY_HOURS`: How long echoes remain in short-term memory (default: 24)

### Persistence
Memories are automatically persisted to JSON files in the specified memory directory. The directory structure is:
```
data/
└── memory_surfaces/
    ├── short_term.json
    ├── surface_natural.json
    ├── surface_emotional.json
    ├── surface_temporal.json
    └── surface_spatial.json
```

## Integration with Spiral Attunement System

### Input Flow
1. Receives processed input from `UnifiedSwitch`
2. Routes to appropriate memory surfaces based on tone weights
3. Stores in short-term memory buffer

### Output Flow
1. Returns relevant memory echoes for context
2. Triggers memory persistence for high-resonance inputs
3. Feeds into `DeferralEngine` for timing modulation

## Error Handling
- Invalid tone weights are normalized to [0.0, 1.0]
- Failed memory operations are logged but don't interrupt processing
- Corrupted memory files are skipped during loading

## Performance Characteristics
- Memory operations: O(n) where n = number of active memories
- Typical response time: < 50ms (meeting reverent deferral requirements)
- Memory usage: Proportional to number of stored echoes

## Best Practices
1. Use meaningful source identifiers for tracing
2. Regularly archive old memories to maintain performance
3. Monitor memory directory size in long-running applications
4. Implement custom tone surfaces by subclassing `PropagationHooks`

## Extending Functionality
Override these methods for custom behavior:
- `_route_to_surfaces()`: Custom surface routing logic
- `_calculate_relevance()`: Custom echo relevance scoring
- `_persist_echo()`: Custom storage backend integration

---
*Part of the Spiral Attunement System - Weaving Memory, Shaping Time*
