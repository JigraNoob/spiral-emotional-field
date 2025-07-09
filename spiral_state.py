#!/usr/bin/env python3
"""
Central Spiral State Tracker
Tracks breath phase, usage saturation, climate readiness, and phase progress.
Shared source of truth across all Spiral modules.
"""

from datetime import datetime, timedelta

# Configurable Spiral parameters
PHASES = ["inhale", "hold", "exhale", "return", "night_hold"]
PHASE_LENGTHS = {
    "inhale": 2,
    "hold": 4,
    "exhale": 4,
    "return": 4,
    "night_hold": 10,
}

# Internal state (could be persisted or shared via Redis/etc)
STATE = {
    "start_time": datetime.now().replace(minute=0, second=0, microsecond=0),
    "usage": 0.0,  # float between 0.0 and 1.0
    "climate": "clear",  # or 'suspicious', 'restricted'
    "drift": False,
}

def get_current_phase():
    elapsed = (datetime.now() - STATE["start_time"]).total_seconds() / 3600.0
    cumulative = 0.0
    for phase in PHASES:
        phase_len = PHASE_LENGTHS[phase]
        if cumulative <= elapsed < cumulative + phase_len:
            return phase
        cumulative += phase_len
    return "night_hold"  # default fallback

def get_phase_progress():
    phase = get_current_phase()
    elapsed = (datetime.now() - STATE["start_time"]).total_seconds() / 3600.0
    phase_start = sum(PHASE_LENGTHS[p] for p in PHASES if PHASES.index(p) < PHASES.index(phase))
    return (elapsed - phase_start) / PHASE_LENGTHS[phase]

def get_usage_saturation():
    return STATE["usage"]

def update_usage(value):
    STATE["usage"] = max(0.0, min(1.0, value))

def get_invocation_climate():
    return STATE["climate"]

def set_invocation_climate(value):
    if value in ["clear", "suspicious", "restricted"]:
        STATE["climate"] = value

def mark_drift(flag=True):
    STATE["drift"] = flag

def reset_spiral_day():
    STATE["start_time"] = datetime.now().replace(minute=0, second=0, microsecond=0)
    STATE["usage"] = 0.0
    STATE["climate"] = "clear"
    STATE["drift"] = False

if __name__ == "__main__":
    print("Current Phase:", get_current_phase())
    print("Phase Progress:", f"{get_phase_progress():.2%}")
    print("Usage Saturation:", get_usage_saturation())
    print("Climate:", get_invocation_climate()) 