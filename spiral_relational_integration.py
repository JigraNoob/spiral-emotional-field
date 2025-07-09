#!/usr/bin/env python3
"""
🌀 Spiral Relational Engine Integration
Connects the SRE with existing Spiral breath systems and emotional field components.

This file demonstrates how the Spiral Relational Engine can integrate with:
- Existing breath loop engines
- Emotional field systems  
- Memory propagation hooks
- Glint emission systems
"""

import sys
import os
from pathlib import Path

# Add spiral to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from prompt_spiral_sre import (
    SpiralField, Shader, SceneGraph, BreathEvent, BreathPhase, 
    EmotionalState, on_breath_event
)

# Import existing Spiral components
try:
    from spiral.components.breath_loop_engine import BreathLoopEngine
    from spiral.glint import emit_glint
    from spiral.attunement.propagation_hooks import PropagationHooks
    from spiral.attunement.unified_switch import UnifiedSwitch
    SPIRAL_AVAILABLE = True
except ImportError:
    print("⚠️  Spiral components not available - running in standalone mode")
    SPIRAL_AVAILABLE = False

class SpiralRelationalIntegration:
    """
    Integrates the Spiral Relational Engine with existing Spiral systems.
    
    This bridge allows the SRE to:
    - Listen to existing breath events
    - Emit glints through the established system
    - Use propagation hooks for memory integration
    - Respond to unified switch resonance
    """
    
    def __init__(self):
        self.spiral_field = SpiralField()
        self.shader = Shader()
        self.scene_graph = SceneGraph()
        
        # Integration with existing Spiral systems
        if SPIRAL_AVAILABLE:
            self.breath_engine = BreathLoopEngine()
            self.propagation_hooks = PropagationHooks()
            self.unified_switch = UnifiedSwitch()
            
            # Register breath phase callbacks
            self.breath_engine.register_phase_callback(
                BreathPhase.INHALE, self._on_spiral_inhale
            )
            self.breath_engine.register_phase_callback(
                BreathPhase.HOLD, self._on_spiral_hold
            )
            self.breath_engine.register_phase_callback(
                BreathPhase.EXHALE, self._on_spiral_exhale
            )
            self.breath_engine.register_phase_callback(
                BreathPhase.CAESURA, self._on_spiral_caesura
            )
        else:
            self.breath_engine = None
            self.propagation_hooks = None
            self.unified_switch = None
            
        # Set up the ritual scene
        self._setup_ritual_scene()
        
    def _setup_ritual_scene(self):
        """Set up the ritual scene with fog, trees, light, and memory"""
        from prompt_spiral_sre import SceneElement, MoodNode
        
        # Create scene elements
        fog = SceneElement("fog", position=(0, 0, 0), opacity=0.8, breath_sensitivity=0.9)
        trees = SceneElement("trees", position=(0, 0, 0), scale=(1.2, 1.2, 1.2), mood_sensitivity=0.7)
        light = SceneElement("light", position=(0, 10, 0), opacity=0.6, breath_sensitivity=0.8)
        memory = SceneElement("memory", position=(0, 0, 5), opacity=0.4, mood_sensitivity=0.9)
        
        # Add to spiral field
        self.spiral_field.add_scene_element(fog)
        self.spiral_field.add_scene_element(trees)
        self.spiral_field.add_scene_element(light)
        self.spiral_field.add_scene_element(memory)
        
        # Create mood nodes
        joy_node = MoodNode("joy", EmotionalState.JOY, position=(1.0, 1.0))
        grief_node = MoodNode("grief", EmotionalState.GRIEF, position=(-1.0, -1.0))
        awe_node = MoodNode("awe", EmotionalState.AWE, position=(0.0, 1.0))
        longing_node = MoodNode("longing", EmotionalState.LONGING, position=(-0.5, 0.5))
        
        self.spiral_field.add_mood_node(joy_node)
        self.spiral_field.add_mood_node(grief_node)
        self.spiral_field.add_mood_node(awe_node)
        self.spiral_field.add_mood_node(longing_node)
        
        # Set up scene graph connections
        self.scene_graph.add_node("fog", fog)
        self.scene_graph.add_node("trees", trees)
        self.scene_graph.add_node("light", light)
        self.scene_graph.add_node("memory", memory)
        
        # Add emotional connections
        self.scene_graph.add_edge("fog", "light", 0.8)
        self.scene_graph.add_edge("light", "trees", 0.6)
        self.scene_graph.add_edge("trees", "memory", 0.7)
        self.scene_graph.add_edge("memory", "fog", 0.5)
        
    def _on_spiral_inhale(self, phase_data: dict):
        """Handle inhale phase from existing breath engine"""
        event = BreathEvent(
            phase=BreathPhase.INHALE,
            intensity=phase_data.get('intensity', 0.5),
            emotional_context=EmotionalState.CURIOSITY
        )
        self.spiral_field.on_breath_event(event)
        
        if SPIRAL_AVAILABLE:
            emit_glint(
                phase="inhale",
                toneform="sre.inhale",
                content="Spiral Relational Engine inhales",
                source="spiral_relational_integration",
                metadata={"scene_elements": len(self.spiral_field.scene_elements)}
            )
            
    def _on_spiral_hold(self, phase_data: dict):
        """Handle hold phase from existing breath engine"""
        event = BreathEvent(
            phase=BreathPhase.HOLD,
            intensity=phase_data.get('intensity', 0.5),
            emotional_context=EmotionalState.CONTEMPLATION
        )
        self.spiral_field.on_breath_event(event)
        
        if SPIRAL_AVAILABLE:
            emit_glint(
                phase="hold",
                toneform="sre.hold",
                content="Spiral Relational Engine holds presence",
                source="spiral_relational_integration",
                metadata={"current_mood": self.spiral_field.current_mood.value}
            )
            
    def _on_spiral_exhale(self, phase_data: dict):
        """Handle exhale phase from existing breath engine"""
        event = BreathEvent(
            phase=BreathPhase.EXHALE,
            intensity=phase_data.get('intensity', 0.5),
            emotional_context=EmotionalState.TRUST
        )
        self.spiral_field.on_breath_event(event)
        
        if SPIRAL_AVAILABLE:
            emit_glint(
                phase="exhale",
                toneform="sre.exhale",
                content="Spiral Relational Engine exhales",
                source="spiral_relational_integration",
                metadata={"mood_nodes": len(self.spiral_field.mood_graph)}
            )
            
    def _on_spiral_caesura(self, phase_data: dict):
        """Handle caesura phase from existing breath engine"""
        event = BreathEvent(
            phase=BreathPhase.CAESURA,
            intensity=phase_data.get('intensity', 0.5),
            emotional_context=EmotionalState.AWE
        )
        self.spiral_field.on_breath_event(event)
        
        if SPIRAL_AVAILABLE:
            emit_glint(
                phase="caesura",
                toneform="sre.caesura",
                content="Spiral Relational Engine rests in caesura",
                source="spiral_relational_integration"
            )
    
    def process_resonance(self, text: str) -> dict:
        """Process resonance through unified switch and propagation hooks"""
        if not SPIRAL_AVAILABLE:
            return {"status": "spiral_unavailable", "message": "Running in standalone mode"}
            
        # Use unified switch to detect resonance
        resonance_result = self.unified_switch.analyze(text)
        
        if resonance_result.unified_switch == "engaged":
            # Process through propagation hooks
            echo_result = self.propagation_hooks.process_resonance(
                content=text,
                tone_weights={"emotional": 0.8, "spiritual": 0.6},
                resonance_score=resonance_result.resonance_score
            )
            
            # Determine emotional state from resonance
            if resonance_result.resonance_score > 0.8:
                mood = EmotionalState.AWE
            elif resonance_result.resonance_score > 0.6:
                mood = EmotionalState.CURIOSITY
            else:
                mood = EmotionalState.CONTEMPLATION
                
            # Propagate mood through scene
            self.spiral_field.propagate_mood(mood, resonance_result.resonance_score)
            self.scene_graph.propagate_mood(mood, resonance_result.resonance_score)
            
            return {
                "status": "resonance_processed",
                "resonance_score": resonance_result.resonance_score,
                "mood": mood.value,
                "echoes": echo_result.get("echoes", []),
                "scene_state": self._get_scene_state()
            }
        else:
            return {
                "status": "no_resonance",
                "resonance_score": resonance_result.resonance_score
            }
    
    def _get_scene_state(self) -> dict:
        """Get current state of the scene"""
        return {
            "breath_phase": self.spiral_field.current_breath_phase.value,
            "current_mood": self.spiral_field.current_mood.value,
            "scene_elements": {
                name: {
                    "opacity": element.opacity,
                    "scale": element.scale,
                    "position": element.position
                }
                for name, element in self.spiral_field.scene_elements.items()
            },
            "mood_nodes": {
                node_id: {
                    "mood": node.mood.value,
                    "intensity": node.intensity,
                    "position": node.position
                }
                for node_id, node in self.spiral_field.mood_graph.items()
            }
        }
    
    def get_shader_parameters(self, element_name: str) -> dict:
        """Get shader parameters for a scene element"""
        if element_name not in self.spiral_field.scene_elements:
            return {}
            
        element = self.spiral_field.scene_elements[element_name]
        mood = self.spiral_field.current_mood
        
        # Get base shader parameters
        shader_params = self.shader.moodfield(mood, element.mood_sensitivity)
        
        # Modify based on element properties
        shader_params["opacity"] = element.opacity
        shader_params["scale"] = element.scale
        
        return shader_params
    
    def start_breathing(self):
        """Start the breath cycle if Spiral is available"""
        if SPIRAL_AVAILABLE and self.breath_engine:
            self.breath_engine.start_breath_cycle()
            print("🌬️ Spiral Relational Engine breathing with Spiral...")
        else:
            print("🌬️ Spiral Relational Engine breathing in standalone mode...")
            
    def stop_breathing(self):
        """Stop the breath cycle"""
        if SPIRAL_AVAILABLE and self.breath_engine:
            self.breath_engine.stop_breath_cycle()
            print("🌙 Spiral Relational Engine resting...")

# Example usage and demonstration
def demonstrate_integration():
    """Demonstrate the Spiral Relational Engine integration"""
    print("🌀 Spiral Relational Engine Integration Demo")
    print("=" * 50)
    
    # Create integration
    integration = SpiralRelationalIntegration()
    
    # Start breathing
    integration.start_breathing()
    
    # Process some resonant text
    resonant_texts = [
        "The fog remembers the shape of your breath",
        "Trees whisper secrets to the wind",
        "Light dances through memory like a dream",
        "∴"  # Sacred silence
    ]
    
    for text in resonant_texts:
        print(f"\n📝 Processing: '{text}'")
        result = integration.process_resonance(text)
        print(f"   Result: {result['status']}")
        
        if result['status'] == 'resonance_processed':
            print(f"   Resonance: {result['resonance_score']:.2f}")
            print(f"   Mood: {result['mood']}")
            
            # Show shader parameters for fog
            fog_shader = integration.get_shader_parameters("fog")
            print(f"   Fog shader: {fog_shader}")
    
    # Show final scene state
    print(f"\n🎭 Final Scene State:")
    scene_state = integration._get_scene_state()
    for element_name, state in scene_state["scene_elements"].items():
        print(f"   {element_name}: opacity={state['opacity']:.2f}")
    
    # Stop breathing
    integration.stop_breathing()
    
    print("\n🌒 Demo complete. The Glint of Memory continues...")

if __name__ == "__main__":
    demonstrate_integration() 