#!/usr/bin/env python3
"""
Simple test of Spiral Relational Engine components
"""

from prompt_spiral_sre import (
    SpiralField, Shader, SceneGraph, BreathEvent, BreathPhase, 
    EmotionalState, SceneElement, MoodNode
)

def test_basic_components():
    """Test basic component creation and functionality"""
    print("🧪 Testing Spiral Relational Engine Components")
    print("=" * 50)
    
    # Test SpiralField
    print("1. Testing SpiralField...")
    field = SpiralField()
    assert field.current_breath_phase == BreathPhase.INHALE
    assert field.current_mood == EmotionalState.CONTEMPLATION
    print("   ✅ SpiralField created successfully")
    
    # Test Shader
    print("2. Testing Shader...")
    shader = Shader()
    params = shader.moodfield(EmotionalState.JOY, 0.8)
    assert "hue" in params
    assert "saturation" in params
    assert "brightness" in params
    print("   ✅ Shader moodfield working")
    
    # Test SceneGraph
    print("3. Testing SceneGraph...")
    scene_graph = SceneGraph()
    assert len(scene_graph.nodes) == 0
    print("   ✅ SceneGraph created successfully")
    
    # Test SceneElement
    print("4. Testing SceneElement...")
    element = SceneElement("test", position=(1, 2, 3), opacity=0.5)
    assert element.name == "test"
    assert element.position == (1, 2, 3)
    assert element.opacity == 0.5
    print("   ✅ SceneElement created successfully")
    
    # Test MoodNode
    print("5. Testing MoodNode...")
    node = MoodNode("test_node", EmotionalState.JOY, intensity=0.7)
    assert node.id == "test_node"
    assert node.mood == EmotionalState.JOY
    assert node.intensity == 0.7
    print("   ✅ MoodNode created successfully")
    
    # Test BreathEvent
    print("6. Testing BreathEvent...")
    event = BreathEvent(phase=BreathPhase.EXHALE, intensity=0.8)
    assert event.phase == BreathPhase.EXHALE
    assert event.intensity == 0.8
    print("   ✅ BreathEvent created successfully")
    
    print("\n🎉 All basic component tests passed!")

def test_scene_interaction():
    """Test scene element interactions"""
    print("\n🎭 Testing Scene Interactions")
    print("=" * 40)
    
    # Create scene
    field = SpiralField()
    shader = Shader()
    
    # Add elements
    fog = SceneElement("fog", opacity=0.8, breath_sensitivity=0.9)
    light = SceneElement("light", opacity=0.6, breath_sensitivity=0.8)
    
    field.add_scene_element(fog)
    field.add_scene_element(light)
    
    # Test breath event
    print("1. Testing breath event...")
    initial_fog_opacity = fog.opacity
    event = BreathEvent(phase=BreathPhase.EXHALE, intensity=0.7)
    field.on_breath_event(event)
    
    # Elements should have responded (even if just pass)
    assert fog.opacity == initial_fog_opacity  # No change in base implementation
    print("   ✅ Breath event processed")
    
    # Test mood propagation
    print("2. Testing mood propagation...")
    initial_light_opacity = light.opacity
    field.propagate_mood(EmotionalState.JOY, 0.8)
    
    # Elements should have responded
    assert light.opacity == initial_light_opacity  # No change in base implementation
    print("   ✅ Mood propagation processed")
    
    print("   ✅ Scene interactions working")

def test_shader_moodfield():
    """Test shader mood field generation"""
    print("\n🎨 Testing Shader Mood Field")
    print("=" * 35)
    
    shader = Shader()
    
    # Test different moods
    moods_to_test = [
        (EmotionalState.JOY, 0.8),
        (EmotionalState.GRIEF, 0.6),
        (EmotionalState.AWE, 0.9),
        (EmotionalState.LONGING, 0.7)
    ]
    
    for mood, intensity in moods_to_test:
        params = shader.moodfield(mood, intensity)
        print(f"   {mood.value}: hue={params['hue']:.0f}°, sat={params['saturation']:.2f}, bright={params['brightness']:.2f}")
        
        # Verify parameters are reasonable
        assert 0 <= params['hue'] <= 360
        assert 0 <= params['saturation'] <= 1
        assert 0 <= params['brightness'] <= 1
        assert params['pulse_rate'] > 0
        assert params['blur_amount'] >= 0
    
    print("   ✅ All mood fields generated successfully")

if __name__ == "__main__":
    test_basic_components()
    test_scene_interaction()
    test_shader_moodfield()
    
    print("\n🌒 All tests completed successfully!")
    print("The Spiral Relational Engine is ready to breathe with you.") 