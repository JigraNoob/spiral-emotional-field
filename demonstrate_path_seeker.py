#!/usr/bin/env python3
"""
🌫️ Path Seeker Demonstration - The Settling Protocol in Action

This script demonstrates the full power of the path_seeker.spiral system:
- How it listens for soil density before it steps
- How it tunes rather than assumes
- How it gathers rather than fetches
- How it makes relational choices based on resonance
"""

import sys
from pathlib import Path
from datetime import datetime
import json

# Import our standalone path seeker
from standalone_path_seeker import SpiralBreathe, SoilDensity, ToneformClimate


def create_test_environment():
    """Create a test environment with different soil characteristics"""
    print("🌱 Creating Test Environment")
    print("=" * 40)
    
    test_dirs = {
        "data": {
            "description": "Rich soil with abundant data",
            "files": ["sample.jsonl", "glint_trace.json", "activity.log"],
            "content": "settling.ambience"
        },
        "archive": {
            "description": "Thin soil with sparse activity", 
            "files": ["old_data.json"],
            "content": "resting.quiet"
        },
        "shrine/storage": {
            "description": "Saturated soil with dense activity",
            "files": ["recent.spiraldata", "active.glint", "current.jsonl", "live_trace.json"],
            "content": "urgent.flow"
        },
        "contemplative_space": {
            "description": "Contemplative soil for reflection",
            "files": ["meditation.md", "reflection.txt", "stillness.json"],
            "content": "contemplative.stillness"
        }
    }
    
    for dir_name, config in test_dirs.items():
        dir_path = Path(dir_name)
        dir_path.mkdir(parents=True, exist_ok=True)
        
        # Create files with content
        for filename in config["files"]:
            file_path = dir_path / filename
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(f"# {config['content']}\n")
                f.write(f"# Created: {datetime.now().isoformat()}\n")
                f.write(f"# Soil type: {config['description']}\n")
        
        print(f"  📁 Created {dir_name}: {config['description']}")


def demonstrate_soil_sensing():
    """Demonstrate how the path seeker senses soil density"""
    print("\n🛤️ Demonstrating Soil Sensing")
    print("=" * 40)
    
    spiral_breathe = SpiralBreathe()
    
    # Test different types of soil
    test_paths = [
        ("Current Directory", Path.cwd()),
        ("Data Directory", Path("data")),
        ("Archive Directory", Path("archive")),
        ("Shrine Storage", Path("shrine/storage")),
        ("Contemplative Space", Path("contemplative_space")),
        ("Nonexistent Path", Path("nonexistent"))
    ]
    
    for name, path in test_paths:
        print(f"\n  👐 Sensing {name}: {path}")
        
        reading = spiral_breathe.grope_path(path)
        
        print(f"    🌱 Soil Density: {reading.density.value}")
        print(f"    🌤️ Toneform Climate: {reading.toneform_climate.value}")
        print(f"    📊 Resonance Score: {reading.resonance_score:.2f}")
        print(f"    📁 Data Presence: {reading.data_presence:.2f}")
        print(f"    ✨ Glint Traces: {len(reading.glint_traces)} found")


def demonstrate_contextual_settling():
    """Demonstrate how the path seeker makes contextual settling decisions"""
    print("\n🏔️ Demonstrating Contextual Settling")
    print("=" * 45)
    
    spiral_breathe = SpiralBreathe()
    
    # Different contexts that might influence settling
    contexts = [
        {
            "name": "Contemplative Context",
            "context": {
                "breath_phase": "hold",
                "required_toneform": "contemplative.stillness",
                "min_resonance": 0.3,
                "intention": "seeking quiet reflection"
            }
        },
        {
            "name": "Urgent Context",
            "context": {
                "breath_phase": "exhale", 
                "required_toneform": "urgent.flow",
                "min_resonance": 0.5,
                "intention": "needing immediate action"
            }
        },
        {
            "name": "Settling Context",
            "context": {
                "breath_phase": "inhale",
                "required_toneform": "settling.ambience", 
                "min_resonance": 0.2,
                "intention": "seeking peaceful presence"
            }
        },
        {
            "name": "General Context",
            "context": {
                "breath_phase": "exhale",
                "intention": "exploring possibilities"
            }
        }
    ]
    
    candidates = [Path("data"), Path("archive"), Path("shrine/storage"), Path("contemplative_space")]
    
    for context_info in contexts:
        print(f"\n  🧭 {context_info['name']}")
        print(f"    Intention: {context_info['context']['intention']}")
        print(f"    Breath Phase: {context_info['context']['breath_phase']}")
        
        decision = spiral_breathe.settle(candidates, context_info['context'])
        
        print(f"    🎯 Chosen Path: {decision.chosen_path}")
        print(f"    📈 Confidence: {decision.confidence:.2f}")
        print(f"    💭 Reasoning: {decision.reasoning}")
        print(f"    🔄 Alternatives: {[str(p) for p in decision.alternatives]}")


def demonstrate_path_guidance():
    """Demonstrate how the path seeker provides guidance"""
    print("\n🧭 Demonstrating Path Guidance")
    print("=" * 40)
    
    spiral_breathe = SpiralBreathe()
    
    # First settle into different paths
    paths_to_explore = [
        ("Data Directory", Path("data")),
        ("Shrine Storage", Path("shrine/storage")),
        ("Contemplative Space", Path("contemplative_space"))
    ]
    
    questions = [
        "What is the current state of this soil?",
        "How should I proceed from here?",
        "What guidance does this path offer?",
        "What is the climate inviting me to do?"
    ]
    
    for path_name, path in paths_to_explore:
        print(f"\n  🏔️ Settling into {path_name}...")
        
        # Settle into this path
        decision = spiral_breathe.settle([path], {"breath_phase": "exhale"})
        print(f"    Settled with confidence: {decision.confidence:.2f}")
        
        # Ask questions of this path
        for question in questions:
            print(f"\n    ❓ Asking: {question}")
            
            response = spiral_breathe.ask(question, {"breath_phase": "hold"})
            
            print(f"      🌱 Soil: {response['soil_density']}")
            print(f"      🌤️ Climate: {response['toneform_climate']}")
            print(f"      📊 Resonance: {response['resonance_level']:.2f}")
            print(f"      💡 Guidance: {response['guidance']}")


def demonstrate_ceremonial_trace():
    """Demonstrate the ceremonial trace of decisions"""
    print("\n📊 Demonstrating Ceremonial Trace")
    print("=" * 40)
    
    spiral_breathe = SpiralBreathe()
    
    # Make several settling decisions to build a trace
    decisions = [
        ("First settling", [Path("data"), Path("archive")], {"breath_phase": "inhale"}),
        ("Second settling", [Path("shrine/storage"), Path("contemplative_space")], {"breath_phase": "hold"}),
        ("Third settling", [Path("data"), Path("shrine/storage")], {"breath_phase": "exhale"}),
        ("Fourth settling", [Path("archive"), Path("contemplative_space")], {"breath_phase": "caesura"})
    ]
    
    print("  🌀 Making ceremonial settling decisions...")
    
    for name, candidates, context in decisions:
        print(f"\n    {name}...")
        decision = spiral_breathe.settle(candidates, context)
        print(f"      Chose: {decision.chosen_path}")
        print(f"      Confidence: {decision.confidence:.2f}")
        print(f"      Phase: {decision.breath_phase}")
    
    # Show the trace
    print(f"\n  📈 Total settling decisions: {len(spiral_breathe.settle_trace)}")
    
    if spiral_breathe.settle_trace:
        print("\n  🕰️ Decision History:")
        for i, decision in enumerate(spiral_breathe.settle_trace[-3:], 1):  # Last 3 decisions
            print(f"    {i}. {decision.chosen_path} (confidence: {decision.confidence:.2f}, phase: {decision.breath_phase})")


def demonstrate_soil_density_spectrum():
    """Demonstrate the full spectrum of soil densities"""
    print("\n🌱 Demonstrating Soil Density Spectrum")
    print("=" * 45)
    
    spiral_breathe = SpiralBreathe()
    
    # Create paths with different characteristics to demonstrate the spectrum
    spectrum_dirs = {
        "void_soil": {
            "description": "Void soil - no resonance, no data",
            "files": [],
            "content": ""
        },
        "thin_soil": {
            "description": "Thin soil - minimal resonance, sparse data",
            "files": ["single_file.txt"],
            "content": "minimal presence"
        },
        "breathable_soil": {
            "description": "Breathable soil - moderate resonance, some data",
            "files": ["data.json", "config.yml", "notes.md"],
            "content": "settling.ambience"
        },
        "rich_soil": {
            "description": "Rich soil - strong resonance, abundant data",
            "files": ["active.jsonl", "glint_trace.json", "recent.spiraldata", "activity.log", "config.json"],
            "content": "urgent.flow"
        },
        "saturated_soil": {
            "description": "Saturated soil - maximum resonance, dense data",
            "files": ["live_trace.json", "active.glint", "current.jsonl", "recent.spiraldata", "activity.log", "config.json", "state.json", "metrics.json"],
            "content": "urgent.flow"
        }
    }
    
    # Create the spectrum
    for dir_name, config in spectrum_dirs.items():
        dir_path = Path(dir_name)
        dir_path.mkdir(parents=True, exist_ok=True)
        
        for filename in config["files"]:
            file_path = dir_path / filename
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(f"# {config['content']}\n")
                f.write(f"# Created: {datetime.now().isoformat()}\n")
    
    # Test each soil type
    print("  🧪 Testing soil density spectrum...")
    
    for dir_name in spectrum_dirs.keys():
        path = Path(dir_name)
        reading = spiral_breathe.grope_path(path)
        
        print(f"\n    {dir_name}:")
        print(f"      Density: {reading.density.value}")
        print(f"      Resonance: {reading.resonance_score:.2f}")
        print(f"      Data Presence: {reading.data_presence:.2f}")


def main():
    """Main demonstration function"""
    print("🌫️ Path Seeker Spiral - The Settling Protocol")
    print("=" * 60)
    print()
    print("This demonstration shows how path_seeker.spiral:")
    print("  • Listens for soil density before it steps")
    print("  • Tunes rather than assumes")
    print("  • Gathers rather than fetches")
    print("  • Makes relational choices based on resonance")
    print()
    
    # Create test environment
    create_test_environment()
    
    # Run demonstrations
    demonstrate_soil_sensing()
    demonstrate_contextual_settling()
    demonstrate_path_guidance()
    demonstrate_ceremonial_trace()
    demonstrate_soil_density_spectrum()
    
    print("\n" + "=" * 60)
    print("🌫️ Demonstration Complete!")
    print("=" * 60)
    print()
    print("The path seeker has demonstrated:")
    print("  ✅ Soil density sensing across different environments")
    print("  ✅ Contextual settling decisions based on breath phase and intention")
    print("  ✅ Path guidance that responds to the current soil state")
    print("  ✅ Ceremonial tracing of all settling decisions")
    print("  ✅ Full spectrum of soil densities from void to saturated")
    print()
    print("This is the quiet revolution:")
    print("  > Code no longer assumes.")
    print("  > It tunes.")
    print("  > It doesn't fetch—it gathers.")
    print()
    print("🌫️ The breath settles into the soil of possibility...")


if __name__ == "__main__":
    main() 