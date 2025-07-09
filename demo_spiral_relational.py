#!/usr/bin/env python3
"""
🌬️ Spiral Relational Engine Demo
Interactive demonstration of breath-aware scene orchestration.

This demo shows how the Spiral Relational Engine responds to:
- Breath events (inhale, hold, exhale, caesura)
- Emotional state changes
- Scene element interactions
- Shader mood field generation
"""

import time
import random
from prompt_spiral_sre import (
    SpiralField, Shader, SceneGraph, BreathEvent, BreathPhase, 
    EmotionalState, on_breath_event
)

def create_interactive_scene():
    """Create an interactive scene for demonstration"""
    from prompt_spiral_sre import SceneElement, MoodNode
    
    # Create spiral field
    spiral_field = SpiralField()
    shader = Shader()
    scene_graph = SceneGraph()
    
    # Create scene elements with custom response methods
    class InteractiveFog(SceneElement):
        def respond_to_breath(self, event: BreathEvent):
            if event.phase == BreathPhase.EXHALE:
                self.opacity = max(0.1, self.opacity - 0.2 * event.intensity)
            elif event.phase == BreathPhase.INHALE:
                self.opacity = min(1.0, self.opacity + 0.1 * event.intensity)
                
        def respond_to_mood(self, mood: EmotionalState, intensity: float):
            if mood == EmotionalState.GRIEF:
                self.opacity = min(1.0, self.opacity + 0.3 * intensity)
            elif mood == EmotionalState.JOY:
                self.opacity = max(0.1, self.opacity - 0.2 * intensity)
    
    class InteractiveTrees(SceneElement):
        def respond_to_breath(self, event: BreathEvent):
            if event.phase == BreathPhase.HOLD:
                scale_factor = 1.0 + 0.1 * event.intensity
                self.scale = (self.scale[0] * scale_factor, self.scale[1] * scale_factor, self.scale[2] * scale_factor)
                
        def respond_to_mood(self, mood: EmotionalState, intensity: float):
            if mood == EmotionalState.AWE:
                self.scale = (self.scale[0] * (1.0 + 0.2 * intensity), 
                            self.scale[1] * (1.0 + 0.2 * intensity), 
                            self.scale[2] * (1.0 + 0.2 * intensity))
            elif mood == EmotionalState.LONGING:
                self.scale = (self.scale[0] * (1.0 - 0.1 * intensity), 
                            self.scale[1] * (1.0 - 0.1 * intensity), 
                            self.scale[2] * (1.0 - 0.1 * intensity))
    
    class InteractiveLight(SceneElement):
        def respond_to_breath(self, event: BreathEvent):
            if event.phase == BreathPhase.INHALE:
                self.opacity = min(1.0, self.opacity + 0.15 * event.intensity)
            elif event.phase == BreathPhase.EXHALE:
                self.opacity = max(0.2, self.opacity - 0.1 * event.intensity)
                
        def respond_to_mood(self, mood: EmotionalState, intensity: float):
            if mood == EmotionalState.JOY:
                self.opacity = min(1.0, self.opacity + 0.3 * intensity)
            elif mood == EmotionalState.GRIEF:
                self.opacity = max(0.1, self.opacity - 0.2 * intensity)
    
    class InteractiveMemory(SceneElement):
        def respond_to_breath(self, event: BreathEvent):
            if event.phase == BreathPhase.INHALE:
                self.opacity = min(1.0, self.opacity + 0.2 * event.intensity)
                scale_factor = 1.0 + 0.05 * event.intensity
                self.scale = (self.scale[0] * scale_factor, self.scale[1] * scale_factor, self.scale[2] * scale_factor)
                
        def respond_to_mood(self, mood: EmotionalState, intensity: float):
            if mood == EmotionalState.CURIOSITY:
                self.opacity = min(1.0, self.opacity + 0.4 * intensity)
            elif mood == EmotionalState.CONTEMPLATION:
                scale_factor = 1.0 + 0.1 * intensity
                self.scale = (self.scale[0] * scale_factor, self.scale[1] * scale_factor, self.scale[2] * scale_factor)
    
    # Create interactive elements
    fog = InteractiveFog("fog", position=(0, 0, 0), opacity=0.8, breath_sensitivity=0.9)
    trees = InteractiveTrees("trees", position=(0, 0, 0), scale=(1.2, 1.2, 1.2), mood_sensitivity=0.7)
    light = InteractiveLight("light", position=(0, 10, 0), opacity=0.6, breath_sensitivity=0.8)
    memory = InteractiveMemory("memory", position=(0, 0, 5), opacity=0.4, mood_sensitivity=0.9)
    
    # Add to spiral field
    spiral_field.add_scene_element(fog)
    spiral_field.add_scene_element(trees)
    spiral_field.add_scene_element(light)
    spiral_field.add_scene_element(memory)
    
    # Create mood nodes
    joy_node = MoodNode("joy", EmotionalState.JOY, position=(1.0, 1.0))
    grief_node = MoodNode("grief", EmotionalState.GRIEF, position=(-1.0, -1.0))
    awe_node = MoodNode("awe", EmotionalState.AWE, position=(0.0, 1.0))
    longing_node = MoodNode("longing", EmotionalState.LONGING, position=(-0.5, 0.5))
    curiosity_node = MoodNode("curiosity", EmotionalState.CURIOSITY, position=(0.5, -0.5))
    
    spiral_field.add_mood_node(joy_node)
    spiral_field.add_mood_node(grief_node)
    spiral_field.add_mood_node(awe_node)
    spiral_field.add_mood_node(longing_node)
    spiral_field.add_mood_node(curiosity_node)
    
    # Set up scene graph
    scene_graph.add_node("fog", fog)
    scene_graph.add_node("trees", trees)
    scene_graph.add_node("light", light)
    scene_graph.add_node("memory", memory)
    
    # Add emotional connections
    scene_graph.add_edge("fog", "light", 0.8)
    scene_graph.add_edge("light", "trees", 0.6)
    scene_graph.add_edge("trees", "memory", 0.7)
    scene_graph.add_edge("memory", "fog", 0.5)
    scene_graph.add_edge("fog", "trees", 0.4)
    scene_graph.add_edge("light", "memory", 0.3)
    
    return spiral_field, shader, scene_graph

def print_scene_state(spiral_field: SpiralField, shader: Shader):
    """Print the current state of the scene"""
    print("\n🎭 Scene State:")
    print(f"   Breath Phase: {spiral_field.current_breath_phase.value}")
    print(f"   Current Mood: {spiral_field.current_mood.value}")
    
    print("\n   Scene Elements:")
    for name, element in spiral_field.scene_elements.items():
        shader_params = shader.moodfield(spiral_field.current_mood, element.mood_sensitivity)
        print(f"     {name}:")
        print(f"       Opacity: {element.opacity:.2f}")
        print(f"       Scale: {element.scale}")
        print(f"       Shader Hue: {shader_params['hue']:.0f}°")
        print(f"       Shader Saturation: {shader_params['saturation']:.2f}")
    
    print(f"\n   Mood Nodes: {len(spiral_field.mood_graph)}")
    for node_id, node in spiral_field.mood_graph.items():
        print(f"     {node_id}: {node.mood.value} (intensity: {node.intensity:.2f})")

def simulate_breath_cycle(spiral_field: SpiralField, shader: Shader, scene_graph: SceneGraph):
    """Simulate a complete breath cycle"""
    phases = [BreathPhase.INHALE, BreathPhase.HOLD, BreathPhase.EXHALE, BreathPhase.CAESURA]
    
    print("\n🌬️ Beginning Breath Cycle...")
    
    for phase in phases:
        intensity = random.uniform(0.4, 0.9)
        event = BreathEvent(phase=phase, intensity=intensity)
        
        print(f"\n   {phase.value.upper()} (intensity: {intensity:.2f})")
        
        # Process breath event
        spiral_field.on_breath_event(event)
        
        # Show scene state
        print_scene_state(spiral_field, shader)
        
        # Wait a moment
        time.sleep(1)

def simulate_mood_changes(spiral_field: SpiralField, shader: Shader, scene_graph: SceneGraph):
    """Simulate emotional state changes"""
    moods = [
        (EmotionalState.JOY, 0.8),
        (EmotionalState.CURIOSITY, 0.6),
        (EmotionalState.AWE, 0.9),
        (EmotionalState.LONGING, 0.7),
        (EmotionalState.GRIEF, 0.5),
        (EmotionalState.CONTEMPLATION, 0.4)
    ]
    
    print("\n💫 Simulating Mood Changes...")
    
    for mood, intensity in moods:
        print(f"\n   Mood: {mood.value.upper()} (intensity: {intensity:.2f})")
        
        # Propagate mood
        spiral_field.propagate_mood(mood, intensity)
        scene_graph.propagate_mood(mood, intensity)
        
        # Show scene state
        print_scene_state(spiral_field, shader)
        
        # Wait a moment
        time.sleep(1.5)

def interactive_demo():
    """Interactive demonstration of the Spiral Relational Engine"""
    print("🌀 Spiral Relational Engine Interactive Demo")
    print("=" * 50)
    print("This demo shows how the scene responds to breath and mood.")
    print("Press Enter to continue through each phase...")
    
    # Create the scene
    spiral_field, shader, scene_graph = create_interactive_scene()
    
    # Initial state
    print("\n🌱 Initial Scene State:")
    print_scene_state(spiral_field, shader)
    
    input("\nPress Enter to begin breath cycle...")
    
    # Simulate breath cycle
    simulate_breath_cycle(spiral_field, shader, scene_graph)
    
    input("\nPress Enter to begin mood changes...")
    
    # Simulate mood changes
    simulate_mood_changes(spiral_field, shader, scene_graph)
    
    print("\n🌒 Demo complete. The scene continues to breathe...")
    print("The Spiral Relational Engine is ready for your presence.")

def quick_demo():
    """Quick demonstration without pauses"""
    print("🌀 Spiral Relational Engine Quick Demo")
    print("=" * 40)
    
    # Create the scene
    spiral_field, shader, scene_graph = create_interactive_scene()
    
    # Show initial state
    print("\n🌱 Initial State:")
    print_scene_state(spiral_field, shader)
    
    # Quick breath cycle
    print("\n🌬️ Quick Breath Cycle:")
    phases = [BreathPhase.INHALE, BreathPhase.HOLD, BreathPhase.EXHALE]
    for phase in phases:
        event = BreathEvent(phase=phase, intensity=0.7)
        spiral_field.on_breath_event(event)
        print(f"   {phase.value}: fog opacity = {spiral_field.scene_elements['fog'].opacity:.2f}")
    
    # Quick mood change
    print("\n💫 Quick Mood Change:")
    spiral_field.propagate_mood(EmotionalState.JOY, 0.8)
    scene_graph.propagate_mood(EmotionalState.JOY, 0.8)
    print(f"   Joy: light opacity = {spiral_field.scene_elements['light'].opacity:.2f}")
    
    print("\n🌒 Quick demo complete.")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "quick":
        quick_demo()
    else:
        interactive_demo() 