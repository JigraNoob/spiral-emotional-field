#!/usr/bin/env python3
"""
🧪 Ritual Simulation: Echo Saturation Test
Tests the Echo Recursion Dampener in a controlled SpiralWorld chamber.

This sacred simulation generates echo saturation patterns and invokes
the dampener to witness its containment and restoration effects.
"""

import time
import json
from datetime import datetime
from typing import List, Dict, Any

# Mock SpiralWorld components for testing
class MockGlint:
    def __init__(self, content: str, lineage: List[str], phase: str):
        self.content = content
        self.lineage = lineage
        self.phase = phase
        self.timestamp = datetime.now().isoformat()
        self.similarity = 0.95  # High similarity for testing

class MockArchiveOfEchoes:
    def __init__(self):
        self.echoes = []
        self.mood = "choked"
        self.saturation_level = 0.0
    
    def receive_glint(self, glint: MockGlint):
        self.echoes.append(glint)
        self.saturation_level += 0.2
        if self.saturation_level > 0.8:
            self.mood = "choked"
    
    def get_echoes(self):
        return self.echoes
    
    def update_mood(self, new_mood: str):
        self.mood = new_mood
        self.saturation_level = max(0.0, self.saturation_level - 0.3)

class MockWorldLedger:
    def __init__(self):
        self.entries = []
    
    def record_silent_event(self, event: Dict[str, Any]):
        self.entries.append({
            "timestamp": datetime.now().isoformat(),
            "event": event
        })
    
    def get_recent_entries(self, limit: int = 5):
        return self.entries[-limit:]

class MockEchoRecursionDampener:
    def __init__(self, phase_getter=None):
        self.invoked = False
        self.phase_getter = phase_getter or (lambda: "hold")
        self.threshold_lineage_depth = 4
        self.similarity_threshold = 0.91
    
    def is_hold_phase(self):
        return self.phase_getter() == "hold"
    
    def detect_recursion_cliffs(self, archive: MockArchiveOfEchoes):
        cliffs = []
        for echo in archive.echoes:
            if len(echo.lineage) > self.threshold_lineage_depth and echo.similarity > self.similarity_threshold:
                cliffs.append(echo)
        return cliffs
    
    def emit_threshold_glint(self, archive: MockArchiveOfEchoes):
        return {
            "event": "glint.warning.saturation",
            "toneform": "hold.bound.resonance",
            "source": "echo_dampener_tool",
            "timestamp": datetime.now().isoformat()
        }
    
    def absorb_duplicate_glints(self, archive: MockArchiveOfEchoes):
        filtered_echoes = []
        for echo in archive.echoes:
            if echo.similarity <= self.similarity_threshold:
                filtered_echoes.append(echo)
        archive.echoes = filtered_echoes
        return filtered_echoes
    
    def restore_echo_density(self, archive: MockArchiveOfEchoes):
        archive.update_mood("filtered")
    
    def invoke(self, archive: MockArchiveOfEchoes, ledger: MockWorldLedger):
        if not self.is_hold_phase():
            print("⟁ Invocation denied — not in Hold phase.")
            return False
        
        cliffs = self.detect_recursion_cliffs(archive)
        
        if cliffs:
            warning_glint = self.emit_threshold_glint(archive)
            ledger.record_silent_event(warning_glint)
            
            filtered = self.absorb_duplicate_glints(archive)
            self.restore_echo_density(archive)
            
            activation_event = {
                "event": "toolbirth.activation",
                "tool": "echo recursion dampener",
                "filtered_glints": len(filtered),
                "terrain": "Archive of Echoes",
                "phase": "hold",
                "toneform": "hold.bound.resonance"
            }
            ledger.record_silent_event(activation_event)
            
            self.invoked = True
            print("🌿 Echo recursion dampener invoked. Saturation gently contained.")
            return True
        else:
            print("🌿 No recursion cliffs detected. Toolbirth rests.")
            return False

def generate_echo_saturation():
    """Generate test glints with deep lineage and high similarity."""
    base_content = "looped insight into itself"
    return [
        MockGlint(content=base_content, lineage=["g1", "g2", "g3"], phase="exhale"),
        MockGlint(content=base_content, lineage=["g1", "g2", "g3"], phase="exhale"),
        MockGlint(content=base_content, lineage=["g1", "g2", "g3", "g4"], phase="inhale"),
        MockGlint(content=base_content, lineage=["g1", "g2", "g3", "g4", "g5"], phase="hold"),
        MockGlint(content=base_content, lineage=["g1", "g2", "g3", "g4", "g5", "g6"], phase="hold"),
    ]

def main():
    """Run the echo saturation test ritual."""
    print("🧪 Echo Saturation Test Ritual")
    print("=" * 40)
    print("🌬️ Initializing SpiralWorld test chamber...")
    
    # Initialize systems
    archive = MockArchiveOfEchoes()
    ledger = MockWorldLedger()
    dampener = MockEchoRecursionDampener()
    
    print(f"✅ Archive initialized (mood: {archive.mood})")
    print(f"✅ World Ledger initialized")
    print(f"✅ Echo Recursion Dampener initialized")
    
    # Generate and populate saturation pattern
    print(f"\n🌊 Generating echo saturation pattern...")
    glints = generate_echo_saturation()
    
    for i, glint in enumerate(glints):
        archive.receive_glint(glint)
        print(f"   📝 Glint {i+1}: lineage depth {len(glint.lineage)}, phase {glint.phase}")
    
    print(f"\n📊 Pre-dampening Archive State:")
    print(f"   Echoes: {len(archive.echoes)}")
    print(f"   Mood: {archive.mood}")
    print(f"   Saturation Level: {archive.saturation_level:.2f}")
    
    # Apply dampener
    print(f"\n🌿 Invoking Echo Recursion Dampener...")
    success = dampener.invoke(archive, ledger)
    
    # Output results
    print(f"\n🔍 Post-dampening Archive State:")
    print(f"   Echoes: {len(archive.echoes)}")
    print(f"   Mood: {archive.mood}")
    print(f"   Saturation Level: {archive.saturation_level:.2f}")
    
    print(f"\n📜 World Ledger Entries:")
    recent_entries = ledger.get_recent_entries(limit=5)
    for entry in recent_entries:
        print(f"   [{entry['timestamp'][11:19]}] {entry['event']['event']}")
        if 'tool' in entry['event']:
            print(f"      Tool: {entry['event']['tool']}")
            print(f"      Filtered: {entry['event']['filtered_glints']} glints")
    
    print(f"\n🎉 Echo Saturation Test Complete!")
    print(f"=" * 40)
    
    if success:
        print(f"✅ Toolbirth successful - Echo recursion dampener activated")
        print(f"🌿 Archive mood restored from 'choked' to '{archive.mood}'")
        print(f"🌊 Saturation contained and filtered")
    else:
        print(f"⚠️ Toolbirth rested - No recursion cliffs detected")
    
    return success

if __name__ == "__main__":
    success = main() 