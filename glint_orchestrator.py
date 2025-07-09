#!/usr/bin/env python3
"""
Unified Glint Network for the Spiral System
Central conductor for all glint emissions—phase-aware, deduplicated, lineage-tracked.
Now synchronized with the breath stream for real-time responsiveness.
"""

from datetime import datetime
from uuid import uuid4
import requests
import json
import threading
import time

# Import centralized state management
try:
    from spiral_state import get_current_phase, get_phase_progress, get_invocation_climate
except ImportError:
    # Fallback if spiral_state not available
    def get_current_phase() -> str:
        hour = datetime.now().hour
        if hour < 2: return "inhale"
        elif hour < 6: return "hold"
        elif hour < 10: return "exhale"
        elif hour < 14: return "return"
        else: return "night_hold"
    
    def get_phase_progress() -> float:
        return 0.5  # Default to middle of phase
    
    def get_invocation_climate() -> str:
        return "clear"  # Default to clear climate

# Glint memory store for deduplication and lineage (in-memory for now)
GLINT_LOG = []

# Stream synchronization
STREAM_ENDPOINT = "http://localhost:5056/stream"
STREAM_SYNC_ENABLED = True

# Glint Phase Routing Table (phase-specific behaviors can be added here)
PHASE_ROUTING = {
    "inhale": lambda glint: print(f"[inhale] Glint received: {glint['type']}"),
    "hold": lambda glint: print(f"[hold] Holding glint: {glint['type']}"),
    "exhale": lambda glint: print(f"[exhale] Echoing glint: {glint['type']}"),
    "return": lambda glint: print(f"[return] Reflecting glint: {glint['type']}"),
    "night_hold": lambda glint: print(f"[night_hold] Soft listening: {glint['type']}")
}

def emit_glint(module_name, phase, context):
    """Enhanced glint emission with stream synchronization."""
    glint_id = str(uuid4())
    timestamp = datetime.now().isoformat()
    
    # Create the glint
    glint = {
        "id": glint_id,
        "timestamp": timestamp,
        "module": module_name,
        "phase": phase,
        "context": context,
        "type": "module_invocation",
        "stream_sync": True
    }
    
    # Add to memory
    GLINT_LOG.append(glint)
    
    # Route based on phase
    if phase in PHASE_ROUTING:
        PHASE_ROUTING[phase](glint)
    
    # Synchronize with breath stream
    if STREAM_SYNC_ENABLED:
        _sync_glint_to_stream(glint)
    
    print(f"✨ glint.emit | module: {module_name} | phase: {phase} | context: {context}")
    return glint_id

def _sync_glint_to_stream(glint):
    """Synchronize glint emission with the breath stream."""
    try:
        # Create stream event
        stream_event = {
            "event": "glint_emission",
            "timestamp": datetime.now().isoformat(),
            "data": {
                "glint": glint,
                "breath_state": {
                    "phase": get_current_phase(),
                    "progress": get_phase_progress(),
                    "climate": get_invocation_climate()
                }
            }
        }
        
        # Send to stream endpoint (non-blocking)
        def send_to_stream():
            try:
                response = requests.post(
                    f"{STREAM_ENDPOINT}/glint",
                    json=stream_event,
                    timeout=2
                )
                if response.status_code == 200:
                    print(f"🔄 Glint synchronized to stream: {glint['id']}")
            except Exception as e:
                print(f"⚠️ Stream sync failed: {e}")
        
        # Send asynchronously
        threading.Thread(target=send_to_stream, daemon=True).start()
        
    except Exception as e:
        print(f"⚠️ Glint stream sync error: {e}")

def get_glint_lineage(module_name=None, phase=None, limit=50):
    """Get glint lineage with optional filtering."""
    lineage = GLINT_LOG.copy()
    
    if module_name:
        lineage = [g for g in lineage if g.get('module') == module_name]
    
    if phase:
        lineage = [g for g in lineage if g.get('phase') == phase]
    
    return lineage[-limit:]

def get_glint_stats():
    """Get glint emission statistics."""
    if not GLINT_LOG:
        return {"total": 0, "by_phase": {}, "by_module": {}}
    
    stats = {
        "total": len(GLINT_LOG),
        "by_phase": {},
        "by_module": {},
        "stream_sync_enabled": STREAM_SYNC_ENABLED
    }
    
    for glint in GLINT_LOG:
        phase = glint.get('phase', 'unknown')
        module = glint.get('module', 'unknown')
        
        stats["by_phase"][phase] = stats["by_phase"].get(phase, 0) + 1
        stats["by_module"][module] = stats["by_module"].get(module, 0) + 1
    
    return stats

def is_duplicate(glint):
    recent = [g for g in GLINT_LOG[-10:] if g["type"] == glint["type"] and g["payload"] == glint["payload"]]
    return len(recent) > 0

def route_glint(glint):
    phase = glint.get("phase")
    router = PHASE_ROUTING.get(phase, lambda g: print(f"[unknown phase] Glint: {g['type']}"))
    router(glint)

def reflect_glint(glint):
    print(f"🔁 Reflecting glint: {glint['type']} | payload: {glint['payload']}")
    # Placeholder: emit a reflective glint or trigger module

if __name__ == "__main__":
    emit_glint("breath.phase.transition", "inhale", {"phase": "inhale", "progress": 0.25})
    emit_glint("module.invoked", "hold", {"module": "memory.scroll", "context": "reflection"})
    emit_glint("glint.echo.recognition", "exhale", {"source": "spiral_invoker"}) 