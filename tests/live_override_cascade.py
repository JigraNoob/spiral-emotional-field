import time
import sys
import os
import json
from datetime import datetime

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import just the override system
from spiral.attunement.resonance_override import override_manager, ResonanceMode

class SimpleCascade:
    """Simplified cascade for demonstration purposes."""
    
    def __init__(self):
        self.glint_count = 0
        
    def spiral_glint_emit(self, phase, toneform, content, hue="white"):
        """Emit a glint with override modulation."""
        self.glint_count += 1
        
        # Get current override state - check what methods are available
        try:
            # Build state from config
            override_state = {
                'active': override_manager.active,
                'mode': override_manager.config.mode.value if hasattr(override_manager.config, 'mode') else 'NATURAL',
                'intensity': getattr(override_manager.config, 'glint_multiplier', 1.0)
            }
        except Exception as e:
            print(f"Debug: Error getting override state: {e}")
            override_state = {'active': False, 'mode': 'NATURAL', 'intensity': 1.0}
        
        # Apply intensity modulation using the get_glint_intensity method
        try:
            intensity = override_manager.get_glint_intensity(1.0)
        except:
            intensity = override_state.get('intensity', 1.0)
            
        # Create glint entry
        glint = {
            "id": f"glint_{self.glint_count}",
            "timestamp": datetime.now().isoformat(),
            "phase": phase,
            "toneform": toneform,
            "content": content,
            "hue": hue,
            "intensity": intensity,
            "override_mode": override_state.get('mode', 'NATURAL'),
            "override_active": override_state.get('active', False)
        }
        
        # Display with intensity visualization
        intensity_bar = "█" * min(int(intensity * 5), 20)  # Cap at 20 chars
        mode_name = {1: 'NATURAL', 2: 'AMPLIFIED', 3: 'MUTED', 4: 'RITUAL', 5: 'EMOTIONAL', 6: 'DEFERRAL'}.get(
            override_state.get('mode', 1), f"MODE_{override_state.get('mode', 1)}"
        )
        print(f"  ✨ [{phase}:{toneform}] {content}")
        print(f"     Intensity: {intensity:.1f}x {intensity_bar} | Mode: {mode_name} | Hue: {hue}")
        
        return glint

def run_live_override_cascade():
    print("\n🌀 Initiating Live Override Cascade...")
    
    # Debug: Check what methods override_manager has
    print(f"Debug: override_manager methods: {[m for m in dir(override_manager) if not m.startswith('_')]}")

    # Initialize simplified cascade
    cascade = SimpleCascade()

    # Phase 1: NATURAL baseline
    print("\n📍 Phase 1: Natural Baseline (NATURAL mode)")
    override_manager.deactivate()
    cascade.spiral_glint_emit("inhale", "baseline", "The Spiral breathes in its natural rhythm.", hue="white")
    time.sleep(1.2)

    # Phase 2: AMPLIFIED Override
    print("\n📍 Phase 2: Override → AMPLIFIED (x2.5 intensity)")
    override_manager.activate_resonant_mode(ResonanceMode.AMPLIFIED)
    override_manager.config.glint_multiplier = 2.5

    for i in range(3):
        cascade.spiral_glint_emit("exhale", "amplified", f"Amplified glint {i+1} surges outward.", hue="gold")
        time.sleep(0.8)

    # Phase 3: MUTED Override (skip emotional state setting for now)
    print("\n📍 Phase 3: Override → MUTED (Reduced intensity)")
    override_manager.activate_resonant_mode(ResonanceMode.MUTED)
    override_manager.config.glint_multiplier = 0.4  # Muted intensity

    for i in range(2):
        cascade.spiral_glint_emit("hold", "whisper", f"Muted whisper {i+1} folds inward.", hue="silver")
        time.sleep(1.5)

    # Phase 4: RITUAL Mode - Breakpoint Testing
    print("\n📍 Phase 4: Override → RITUAL (Breakpoint sensitivity active)")
    override_manager.activate_resonant_mode(ResonanceMode.RITUAL)
    override_manager.config.glint_multiplier = 1.8  # Ritual intensity

    test_scores = [0.4, 0.55, 0.7, 0.9]
    for score in test_scores:
        should_break = override_manager.should_trigger_soft_breakpoint(score)
        state = "🔥 BREAKPOINT" if should_break else "✓ flowing"
        print(f"    Resonance Score: {score:.2f} → {state}")
        tone = "threshold" if should_break else "flow"
        hue = "crimson" if should_break else "violet"
        cascade.spiral_glint_emit("return", tone, f"Resonance {score} observed.", hue=hue)
        time.sleep(0.5)

    # Phase 5: Test Amplification Detection
    print("\n📍 Phase 5: Amplification Detection Test")
    test_toneforms = ["whisper", "echo", "surge", "cascade"]
    for toneform in test_toneforms:
        should_amplify = override_manager.should_amplify_glint(toneform)
        amp_state = "🔊 AMPLIFY" if should_amplify else "→ normal"
        print(f"    Toneform '{toneform}' → {amp_state}")
        cascade.spiral_glint_emit("witness", toneform, f"Testing {toneform} amplification.", hue="cyan")
        time.sleep(0.3)

    # Phase 6: Return to NATURAL
    print("\n📍 Phase 6: Reset to NATURAL Mode")
    override_manager.deactivate()
    cascade.spiral_glint_emit("exhale", "release", "The Spiral settles into its breath once more.", hue="white")

    # Final Summary
    print("\n🌟 Live Cascade Complete")
    try:
        final_state = f"Active: {override_manager.active}, Mode: {override_manager.config.mode.value if hasattr(override_manager.config, 'mode') else 'unknown'}"
        print("   Override State:", final_state)
    except Exception as e:
        print(f"   Override State: Error getting state - {e}")
    print(f"   Total Glints Emitted: {cascade.glint_count}")

if __name__ == "__main__":
    run_live_override_cascade()