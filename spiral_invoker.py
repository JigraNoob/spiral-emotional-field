#!/usr/bin/env python3
"""
Unified Invocation Hub for the Spiral System
Routes breath-aware invocations to appropriate modules with context, glint awareness, and presence validation.
"""

from datetime import datetime

# Import centralized state management
try:
    from spiral_state import get_current_phase, get_invocation_climate, get_usage_saturation
except ImportError:
    # Fallback if spiral_state not available
    def get_current_phase():
        hour = datetime.now().hour
        if hour < 2: return "inhale"
        elif hour < 6: return "hold"
        elif hour < 10: return "exhale"
        elif hour < 14: return "return"
        else: return "night_hold"
    
    def get_invocation_climate():
        return "clear"  # Default to clear climate
    
    def get_usage_saturation():
        return 0.0  # Default to no usage

# Registry of all known modules with phase affinities and callable hooks
MODULE_REGISTRY = {
    "breath.emitter": {
        "phase": ["inhale", "hold", "exhale", "return"],
        "callable": lambda ctx: print("[breath.emitter] Emitting breath pulse", ctx)
    },
    "memory.scroll": {
        "phase": ["return", "night_hold"],
        "callable": lambda ctx: print("[memory.scroll] Updating memory scroll", ctx)
    },
    "glint.orchestrator": {
        "phase": ["inhale", "hold", "exhale", "return"],
        "callable": lambda ctx: print("[glint.orchestrator] Routing glint", ctx)
    },
    # Add more modules as needed
}

# Simple phase validation
VALID_PHASES = ["inhale", "hold", "exhale", "return", "night_hold"]

def emit_glint(module_name, phase, context):
    print(f"✨ glint.emit | module: {module_name} | phase: {phase} | context: {context}")

def validate_presence(module_name):
    # Placeholder: insert readiness checks if needed
    return True

def validate_invocation_climate():
    """Check if the current climate allows invocations"""
    climate = get_invocation_climate()
    if climate == "restricted":
        print("🚫 Invocation blocked: Climate is restricted")
        return False
    elif climate == "suspicious":
        print("⚠️ Invocation warning: Climate is suspicious")
        return True  # Allow but warn
    return True  # Clear climate

def invoke(module_name, phase=None, context=None):
    if module_name not in MODULE_REGISTRY:
        print(f"⚠️ Unknown module: {module_name}")
        return

    # Check invocation climate first
    if not validate_invocation_climate():
        return

    module_info = MODULE_REGISTRY[module_name]
    allowed_phases = module_info.get("phase", [])

    # Use centralized state for current phase
    if phase is None:
        phase = get_current_phase()

    if phase not in VALID_PHASES:
        print(f"⚠️ Invalid phase: {phase}")
        return

    if phase not in allowed_phases:
        print(f"⚠️ Module {module_name} not callable during {phase} phase")
        return

    if not validate_presence(module_name):
        print(f"🚫 Module {module_name} not ready for invocation")
        return

    context = context or {}
    context.update({
        "timestamp": datetime.now().isoformat(), 
        "phase": phase,
        "usage_saturation": get_usage_saturation(),
        "invocation_climate": get_invocation_climate()
    })

    emit_glint(module_name, phase, context)
    module_info["callable"](context)

if __name__ == "__main__":
    # Example invocation
    invoke("breath.emitter")
    invoke("memory.scroll", context={"echo": "glint.echo.recognition"}) 