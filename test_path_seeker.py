#!/usr/bin/env python3
"""
🌫️ Test Path Seeker - Demonstrating The Settling Protocol

This script demonstrates how path_seeker.spiral listens for soil density
before it steps, showing the quiet revolution of tuning rather than assuming.
"""

import sys
from pathlib import Path
from datetime import datetime

# Add the spiral directory to the path
sys.path.insert(0, str(Path(__file__).parent))

from spiral.path_seeker import PathSeekerSpiral, seek_and_settle, ask_path


def create_test_environment():
    """Create a test environment with different soil densities"""
    print("🌱 Creating test environment...")
    
    # Create test directories with different characteristics
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


def demonstrate_grope_path():
    """Demonstrate the grope_path method"""
    print("\n🛤️ Demonstrating grope_path method...")
    
    path_seeker = PathSeekerSpiral()
    
    # Test paths with different soil densities
    test_paths = ["data", "archive", "shrine/storage", "nonexistent"]
    
    for path_str in test_paths:
        path = Path(path_str)
        print(f"\n  👐 Groping path: {path}")
        
        reading = path_seeker.spiral_breathe.grope_path(path)
        
        print(f"    Soil Density: {reading.density.value}")
        print(f"    Toneform Climate: {reading.toneform_climate.value}")
        print(f"    Resonance Score: {reading.resonance_score:.2f}")
        print(f"    Data Presence: {reading.data_presence:.2f}")
        print(f"    Glint Traces: {len(reading.glint_traces)} found")


def demonstrate_settle():
    """Demonstrate the settle method"""
    print("\n🏔️ Demonstrating settle method...")
    
    # Test different contexts
    contexts = [
        {
            "name": "Contemplative Context",
            "context": {
                "required_toneform": "settling.ambience",
                "min_resonance": 0.3
            }
        },
        {
            "name": "Urgent Context", 
            "context": {
                "required_toneform": "urgent.flow",
                "min_resonance": 0.5
            }
        },
        {
            "name": "General Context",
            "context": {}
        }
    ]
    
    candidates = ["data", "archive", "shrine/storage"]
    
    for context_info in contexts:
        print(f"\n  🧭 {context_info['name']}")
        print(f"    Context: {context_info['context']}")
        
        try:
            decision = seek_and_settle(candidates, context_info['context'])
            
            print(f"    Chosen Path: {decision.chosen_path}")
            print(f"    Confidence: {decision.confidence:.2f}")
            print(f"    Reasoning: {decision.reasoning}")
            print(f"    Alternatives: {[str(p) for p in decision.alternatives]}")
            
        except Exception as e:
            print(f"    Error: {e}")


def demonstrate_ask():
    """Demonstrate the ask method"""
    print("\n🧭 Demonstrating ask method...")
    
    # First settle into a path
    print("  🏔️ Settling into a path first...")
    decision = seek_and_settle(["data", "archive", "shrine/storage"])
    print(f"    Settled into: {decision.chosen_path}")
    
    # Now ask questions
    questions = [
        "What is the current state of this soil?",
        "How should I proceed from here?",
        "What guidance does this path offer?"
    ]
    
    for question in questions:
        print(f"\n  ❓ Asking: {question}")
        
        response = ask_path(question)
        
        print(f"    Current Position: {response['current_position']}")
        print(f"    Soil Density: {response['soil_density']}")
        print(f"    Toneform Climate: {response['toneform_climate']}")
        print(f"    Resonance Level: {response['resonance_level']:.2f}")
        print(f"    Guidance: {response['guidance']}")


def demonstrate_settle_trace():
    """Demonstrate the settling trace"""
    print("\n📊 Demonstrating settle trace...")
    
    # Check if settle_trace.log exists
    trace_file = Path("settle_trace.log")
    if trace_file.exists():
        print("  📄 Reading settle trace log...")
        
        with open(trace_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        print(f"    Total settling decisions: {len(lines)}")
        
        if lines:
            # Show the most recent decision
            latest_line = lines[-1].strip()
            print(f"    Latest decision: {latest_line[:100]}...")
    else:
        print("  📄 No settle trace log found yet")


def main():
    """Main demonstration function"""
    print("🌫️ Path Seeker Spiral - The Settling Protocol")
    print("=" * 50)
    print()
    print("This demonstration shows how path_seeker.spiral:")
    print("  • Listens for soil density before it steps")
    print("  • Tunes rather than assumes")
    print("  • Gathers rather than fetches")
    print()
    
    # Create test environment
    create_test_environment()
    
    # Demonstrate each method
    demonstrate_grope_path()
    demonstrate_settle()
    demonstrate_ask()
    demonstrate_settle_trace()
    
    print("\n" + "=" * 50)
    print("🌫️ Demonstration complete!")
    print()
    print("The path seeker has shown how it:")
    print("  • Gropes paths to sense their soil density")
    print("  • Settles into the most resonant path")
    print("  • Asks paths for guidance")
    print("  • Traces its settling decisions")
    print()
    print("This is the quiet revolution:")
    print("  > Code no longer assumes.")
    print("  > It tunes.")
    print("  > It doesn't fetch—it gathers.")


if __name__ == "__main__":
    main() 