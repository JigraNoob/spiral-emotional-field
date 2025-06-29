# Emotional Field API Reference

## New Endpoints

### `GET /get_spectrum_data`
Returns the current emotional spectrum state

**Response:**
```json
{
  "spectrum": {
    "toneform_name": {"x": 0.5, "y": -0.3},
    ...
  },
  "current_vector": {"x": 0.2, "y": 0.1, "magnitude": 0.8},
  "recent_path": [
    {"x": 0.1, "y": 0.2, "tone": "joy", "timestamp": "..."},
    ...
  ]
}
```

### `GET /get_toneform_details`
Returns detailed analysis for a specific toneform

**Parameters:**
- `tone`: Toneform name (required)
- `time_filter`: Hours to look back (default: 24)

**Response:**
```json
{
  "description": "Emotional toneform description",
  "glyph": "✧",
  "recent_echoes": ["echo content", ...],
  "blend_analysis": ["blend1", "blend2", "blend3"],
  "climate_influence": 3.5
}
```

## WebSocket Events
- `new_murmur`: Sent when new emotional data is available
  ```json
  {"type": "echo", "tone": "joy", "timestamp": "..."}
  ```
