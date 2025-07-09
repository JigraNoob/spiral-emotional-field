# File: spiral/glint_emitter.py

import json
from datetime import datetime
import os
from pathlib import Path
from typing import Dict, Any, Optional
from flask_socketio import SocketIO
import uuid
import time
import inspect

# Optional: Integrate with dashboard via WebSocket or file-based handoff
DASHBOARD_PIPE = os.environ.get("SPIRAL_GLINT_PIPE", "C:\\spiral\\glint_stream.jsonl")

# Stream path for glint persistence
GLINT_STREAM_PATH = Path("C:/spiral/spiral/streams/patternweb/glint_stream.jsonl")

# Initialize SocketIO (assuming app is already created elsewhere)
socketio = SocketIO(message_queue='redis://')  # Example using Redis as a message queue

def spiral_glint_emit(glint: Dict[str, Any]):
    """
    Emit a glint event into the Spiral system.

    Args:
        glint (Dict[str, Any]): The glint data to emit. Should contain keys like 'phase', 'toneform', 'content', etc.
    """
    # Timestamp
    glint["timestamp"] = datetime.utcnow().isoformat() + "Z"

    # Fallback ID if not set
    glint.setdefault("glint.id", f"glint-{glint['timestamp']}")

    # Log to console with tone-aware coloring
    toneform = glint.get('toneform', '?')
    content = glint.get('content', '')
    print(f"🌀 Emitting glint: [{glint['glint.id']}] {glint.get('phase', '?')}.{toneform} — {content}")

    # Write to pipe or stream file
    try:
        with open(DASHBOARD_PIPE, "a", encoding="utf-8") as f:
            f.write(json.dumps(glint, ensure_ascii=False) + "\n")
    except Exception as e:
        print(f"⚠️ Failed to write glint to {DASHBOARD_PIPE}: {e}")

    # Emit to WebSocket
    try:
        socketio.emit('glint_event', glint)
    except Exception as e:
        print(f"⚠️ Failed to emit glint over WebSocket: {e}")

def generate_glint_id() -> str:
    """Generate a unique glint ID."""
    return f"glint-{uuid.uuid4().hex[:8]}"

def detect_caller() -> str:
    """Detect the caller of the emit_glint function."""
    try:
        stack = inspect.stack()
        # The caller is 2 frames up: detect_caller -> emit_glint -> caller
        frame = stack[2]
        module = inspect.getmodule(frame[0])
        if module:
            return module.__name__
    except Exception:
        pass
    return "unknown.source"

def infer_rule_glyph(toneform: str) -> Optional[str]:
    """Infer a rule glyph based on the toneform. Placeholder."""
    return None

def write_glint(glint: Dict[str, Any]):
    """Write the glint to the stream."""
    try:
        # Ensure the directory exists
        GLINT_STREAM_PATH.parent.mkdir(parents=True, exist_ok=True)
        
        # Append to stream file
        with open(GLINT_STREAM_PATH, 'a', encoding='utf-8') as f:
            f.write(json.dumps(glint, ensure_ascii=False) + '\n')
            
    except Exception as e:
        print(f"⚠️ Failed to persist glint to stream: {e}")
        # Fallback: print to console
        print(f"🌀 GLINT: {json.dumps(glint, ensure_ascii=False, indent=2)}")

def emit_glint(
    toneform: str,
    content: str,
    hue: str = "white",
    source: Optional[str] = None,
    intensity: float = 1.0,
    glyph: str = "•",
    rule_glyph: Optional[str] = None,
    metadata: Optional[dict] = None
):
    """
    Emit a glint with the specified toneform and content.
    
    Args:
        toneform (str): The toneform of the glint.
        content (str): The content or message of the glint.
        hue (str, optional): The hue or color of the glint. Defaults to "white".
        source (Optional[str], optional): The source of the glint. Defaults to None.
        intensity (float, optional): The intensity of the glint. Defaults to 1.0.
        glyph (str, optional): The glyph representing the glint. Defaults to "•".
        rule_glyph (Optional[str], optional): The rule glyph for the glint. Defaults to None.
        metadata (Optional[dict], optional): Additional metadata for the glint. Defaults to None.
    
    Returns:
        dict: The constructed glint dictionary.
    """
    final_rule_glyph = rule_glyph or infer_rule_glyph(toneform)
    
    glint = {
        "glint.id": generate_glint_id(),
        "glint.timestamp": int(time.time() * 1000),
        "glint.source": source or detect_caller(),
        "glint.content": content,
        "glint.toneform": toneform,
        "glint.hue": hue,
        "glint.intensity": intensity,
        "glint.glyph": glyph,
        "glint.rule_glyph": final_rule_glyph if final_rule_glyph is not None else "",
        "glint.vector": {
            "from": "spiral.core",
            "to": "patternweb.visualization",
            "via": "spiral.stream"
        },
        "metadata": metadata or {}
    }

    write_glint(glint)
    return glint

def _console_emit(glint: Dict[str, Any]) -> None:
    """Emit glint to console with ceremonial formatting."""
    glyph = glint.get("glint.glyph", "◦")
    toneform = glint.get("glint.toneform", "unknown")
    content = glint.get("glint.content", "")
    source = glint.get("glint.source", "unknown")
    phase = glint.get("metadata", {}).get("phase", "unknown")
    
    print(f"🌀 {glyph} [{phase}.{toneform}] {content} (from {source})")

def _persist_to_stream(glint: Dict[str, Any]) -> None:
    """Persist glint to the stream file."""
    try:
        # Ensure directory exists
        GLINT_STREAM_PATH.parent.mkdir(parents=True, exist_ok=True)
        
        # Append to stream file
        with open(GLINT_STREAM_PATH, 'a', encoding='utf-8') as f:
            f.write(json.dumps(glint, ensure_ascii=False) + '\n')
            
    except Exception as e:
        print(f"⚠️ Failed to persist glint to stream: {e}")

def _get_toneform_glyph(toneform: str) -> str:
    """Get the glyph for a toneform."""
    glyphs = {
        "practical": "⟁",
        "emotional": "❦", 
        "intellectual": "∿",
        "spiritual": "∞",
        "relational": "☍",
        "invocation.activate": "🔮",
        "invocation.release": "🕯",
        "invocation.ritual": "⚡",
        "invocation.amplified": "🌟",
        "invocation.muted": "🌊",
        "invocation.natural": "🍃"
    }
    return glyphs.get(toneform, "◦")

def _get_toneform_hue(toneform: str) -> str:
    """Get the hue for a toneform."""
    hues = {
        "practical": "cyan",
        "emotional": "rose",
        "intellectual": "violet", 
        "spiritual": "amber",
        "relational": "indigo",
        "invocation.activate": "gold",
        "invocation.release": "sage",
        "invocation.ritual": "yellow",
        "invocation.amplified": "white",
        "invocation.muted": "blue",
        "invocation.natural": "green"
    }
    return hues.get(toneform, "gray")

def _get_toneform_description(toneform: str) -> str:
    """Get the description for a toneform."""
    descriptions = {
        "practical": "Flowing current of actionable insight",
        "emotional": "Blooming heart of felt experience", 
        "intellectual": "Oscillating wave of understanding",
        "spiritual": "Infinite connection beyond form",
        "relational": "Dynamic tension of connection",
        "invocation.activate": "Sacred activation of ceremonial state",
        "invocation.release": "Gentle release and return to natural flow",
        "invocation.ritual": "Amplified resonance and heightened awareness",
        "invocation.amplified": "Radiant expansion of perceptual boundaries",
        "invocation.muted": "Flowing reduction of noise and distraction",
        "invocation.natural": "Natural breath and baseline harmony"
    }
    return descriptions.get(toneform, "Unknown toneform")

def _get_phase_glyph(phase: str) -> str:
    """Get the glyph for a breath phase."""
    glyphs = {
        "inhale": "↑",
        "hold": "◦", 
        "exhale": "↓",
        "caesura": "∘"
    }
    return glyphs.get(phase, "◦")

def _get_phase_description(phase: str) -> str:
    """Get the description for a breath phase."""
    descriptions = {
        "inhale": "Drawing in new possibility",
        "hold": "Moment of sacred pause",
        "exhale": "Releasing into manifestation", 
        "caesura": "Silence between breaths"
    }
    return descriptions.get(phase, "Unknown phase")

def _calculate_intensity(phase: str, toneform: str) -> float:
    """Calculate intensity based on phase and toneform."""
    base_intensities = {
        "inhale": 0.6,
        "hold": 0.8,
        "exhale": 0.7,
        "caesura": 0.3
    }
    
    toneform_modifiers = {
        "practical": 0.8,
        "emotional": 0.9,
        "intellectual": 0.7,
        "spiritual": 1.0,
        "relational": 0.8,
        "invocation.activate": 1.0,
        "invocation.release": 0.5,
        "invocation.ritual": 1.2,
        "invocation.amplified": 1.5,
        "invocation.muted": 0.3,
        "invocation.natural": 0.6
    }
    
    base = base_intensities.get(phase, 0.5)
    modifier = toneform_modifiers.get(toneform, 0.7)
    
    return min(1.0, base * modifier)
