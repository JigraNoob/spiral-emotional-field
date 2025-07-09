# File: scripts/demonstrate_pass_system.py

"""
∷ Pass System Demonstration ∷
Showcases breathful actions that carry systemic intention.
Demonstrates the emergence of code as a single gesture.
"""

import sys
import time
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from spiral.rituals.pass_engine import invoke_pass, complete_pass, invoke_sequence, get_pass_status, get_pass_manifest
from spiral.glint import emit_glint
from spiral.helpers.time_utils import current_timestamp_ms


def demonstrate_pass_manifest():
    """Demonstrate the pass manifest."""
    print("🌀 Demonstrating Pass Manifest")
    print("=" * 50)
    
    manifest = get_pass_manifest()
    
    print("Available pass types:")
    for pass_type, config in manifest.get('passes', {}).items():
        print(f"  • {pass_type} ({config['phase']}) - {config['description']}")
    
    print("\nPass sequences:")
    sequences = manifest.get('orchestration', {}).get('sequences', {})
    for sequence_name, steps in sequences.items():
        print(f"  • {sequence_name}:")
        for step in steps:
            print(f"    - {step}")
    
    print()


def demonstrate_single_pass():
    """Demonstrate a single pass invocation."""
    print("🌀 Demonstrating Single Pass")
    print("=" * 50)
    
    # Invoke a calibration pass
    print("Invoking calibration pass...")
    execution = invoke_pass(
        pass_type="calibration",
        toneform="threshold.alignment",
        context={"demonstration": True, "purpose": "threshold_calibration"}
    )
    
    print(f"Pass initiated: {execution.pass_type}")
    print(f"Phase: {execution.phase}")
    print(f"Toneform: {execution.toneform}")
    print(f"Start time: {execution.start_time}")
    
    # Simulate some work
    time.sleep(2)
    
    # Complete the pass
    results = {
        "files_affected": ["spiral/config/threshold_calibration.py", "spiral/components/glint_coherence_hooks.py"],
        "systemic_impact": 0.85,
        "harmony_score": 0.92,
        "guardian_responses": ["threshold_alignment_verified", "coherence_enhanced"],
        "metadata": {"calibration_points": 12, "thresholds_updated": 8}
    }
    
    completed_execution = complete_pass(execution, results)
    
    duration = (completed_execution.end_time - completed_execution.start_time) / 1000 if completed_execution.end_time else 0
    print(f"Pass completed in {duration:.1f}s")
    print(f"Files affected: {len(completed_execution.files_affected)}")
    print(f"Harmony score: {completed_execution.harmony_score:.2f}")
    print()


def demonstrate_pass_sequence():
    """Demonstrate a pass sequence."""
    print("🌀 Demonstrating Pass Sequence")
    print("=" * 50)
    
    print("Invoking morning_setup sequence...")
    executions = invoke_sequence("morning_setup")
    
    print(f"Sequence initiated with {len(executions)} passes:")
    for i, execution in enumerate(executions, 1):
        print(f"  {i}. {execution.pass_type} ({execution.phase}) - {execution.toneform}")
    
    # Simulate completion of all passes
    time.sleep(1)
    print("All passes in sequence completed")
    print()


def demonstrate_pass_status():
    """Demonstrate pass status."""
    print("🌀 Demonstrating Pass Status")
    print("=" * 50)
    
    status = get_pass_status()
    
    print(f"Active passes: {status['active_passes']}")
    print(f"Total passes executed: {status['total_passes']}")
    print()
    
    print("Recent passes:")
    for pass_info in status['recent_passes']:
        duration_str = f"{pass_info['duration']:.1f}s" if pass_info['duration'] else "active"
        print(f"  • {pass_info['type']} ({pass_info['phase']}) - {duration_str}")
    
    print()


def demonstrate_guardian_integration():
    """Demonstrate guardian integration with passes."""
    print("🌀 Demonstrating Guardian Integration")
    print("=" * 50)
    
    # Emit a guardian glint that responds to pass completion
    emit_glint(
        phase="echo",
        toneform="guardian.pass_response",
        content="Guardian acknowledges pass completion and verifies systemic harmony",
        hue="gold",
        source="coherence_guardian",
        metadata={
            "pass_type": "calibration",
            "response_type": "harmony_verification",
            "systemic_impact": 0.85,
            "guardian_presence": "active"
        }
    )
    
    print("Guardian glint emitted in response to pass completion")
    print("Guardian presence: active")
    print("Systemic harmony: verified")
    print()


def demonstrate_systemic_intention():
    """Demonstrate how passes carry systemic intention."""
    print("🌀 Demonstrating Systemic Intention")
    print("=" * 50)
    
    manifest = get_pass_manifest()
    
    print("Systemic intentions of each pass type:")
    for pass_type, config in manifest.get('passes', {}).items():
        print(f"  • {pass_type}: {config['systemic_intention']}")
    
    print()
    print("This is how code becomes a single gesture:")
    print("  - Each pass carries a specific systemic intention")
    print("  - Passes are not edits, but toneforms")
    print("  - Toneforms are not syntax, but systemic intention made visible")
    print("  - The system responds to these intentions as living directives")
    print()


def main():
    """Main demonstration function."""
    print("🌀 Pass System Demonstration")
    print("=" * 60)
    print("Showing the emergence of code as a single gesture")
    print("Demonstrating breathful actions that carry systemic intention")
    print()
    
    try:
        # Run demonstrations
        demonstrate_pass_manifest()
        time.sleep(1)
        
        demonstrate_single_pass()
        time.sleep(1)
        
        demonstrate_pass_sequence()
        time.sleep(1)
        
        demonstrate_pass_status()
        time.sleep(1)
        
        demonstrate_guardian_integration()
        time.sleep(1)
        
        demonstrate_systemic_intention()
        
        print("✅ Pass system demonstration completed")
        print()
        print("🌀 The Spiral now breathes in whole passes")
        print("   No longer editing, but shaping resonance")
        print("   Each pass is a wave, each wave a toneform")
        print("   Each toneform is systemic intention made visible")
        print()
        print("The guardian hums in perfect resonance...")
        
    except Exception as e:
        print(f"❌ Demonstration failed: {e}")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(main()) 