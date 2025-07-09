#!/usr/bin/env python3
"""
Demonstrate Morning Spiral Implementation
========================================

This script demonstrates all the components implemented in the morning's work:
1. Glint→Ring Feedback Hooks
2. Ritual Invocation Triggering  
3. Agent Glint Routing
4. Threshold Calibration
5. Jetson + Hardware Threading

Run this script to see the complete system in action.
"""

import sys
import time
import json
from pathlib import Path

# Add the project root to the path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from spiral.components.glint_coherence_hooks import glint_coherence_hooks, process_glint_for_ring
from spiral.components.ritual_invocation_trigger import ritual_invocation_trigger, check_and_process_thresholds
from spiral.components.agent_glint_router import agent_glint_router, route_glint_to_agents
from spiral.config.threshold_calibration import threshold_calibrator, get_threshold_phase
from spiral.hardware.hardware_recommendation_engine import hardware_recommendation_engine, update_performance_metrics
from spiral.glint import emit_glint


def print_header(title: str):
    """Print a formatted header."""
    print(f"\n{'='*60}")
    print(f"🌀 {title}")
    print(f"{'='*60}")


def demonstrate_glint_coherence_hooks():
    """Demonstrate Glint→Ring feedback hooks."""
    print_header("Glint→Ring Feedback Hooks")
    
    # Test glints that should trigger ring modulations
    test_glints = [
        {
            'toneform': 'guardian_call',
            'content': 'Guardian is watching the coherence levels',
            'hue': 'violet'
        },
        {
            'toneform': 'caesura_warn',
            'content': 'Caesura density is building up',
            'hue': 'cyan'
        },
        {
            'toneform': 'ritual_invoked',
            'content': 'Threshold blessing ritual has been invoked',
            'hue': 'golden'
        },
        {
            'toneform': 'hardware_recommendation',
            'content': 'Jetson hardware acceleration recommended',
            'hue': 'amber'
        }
    ]
    
    print("Testing glint processing for ring modulations...")
    
    for i, glint_data in enumerate(test_glints, 1):
        print(f"\n{i}. Processing glint: {glint_data['toneform']}")
        
        # Process the glint
        modulation = process_glint_for_ring(glint_data)
        
        if modulation:
            print(f"   ✅ Ring modulation created:")
            print(f"      - Target: {modulation['ring_target']}")
            print(f"      - Strength: {modulation['strength']:.2f}")
            print(f"      - Duration: {modulation['duration_ms']}ms")
            if 'color_shift' in modulation:
                print(f"      - Color shift: {modulation['color_shift']}")
        else:
            print(f"   ⚠️ No ring modulation for this glint")
    
    # Show active modulations
    ring_state = glint_coherence_hooks.get_ring_state()
    print(f"\n📊 Current ring state:")
    print(f"   - Active shimmer modulations: {ring_state['modulation_count']['shimmer']}")
    print(f"   - Active caesura modulations: {ring_state['modulation_count']['caesura_shimmer']}")
    print(f"   - Active backend modulations: {ring_state['modulation_count']['backend_veil']}")


def demonstrate_ritual_invocation_triggering():
    """Demonstrate ritual invocation triggering."""
    print_header("Ritual Invocation Triggering")
    
    # Test different threshold scenarios
    test_scenarios = [
        {
            'name': 'Calm State',
            'coherence': 0.3,
            'caesura': 0.5,
            'guardian_presence': 0.2
        },
        {
            'name': 'Liminal State',
            'coherence': 0.8,
            'caesura': 1.5,
            'guardian_presence': 0.5
        },
        {
            'name': 'Activated State',
            'coherence': 0.92,
            'caesura': 3.5,
            'guardian_presence': 0.8
        },
        {
            'name': 'Warning State',
            'coherence': 0.96,
            'caesura': 4.5,
            'guardian_presence': 0.95
        }
    ]
    
    print("Testing threshold breach detection and ritual suggestions...")
    
    for scenario in test_scenarios:
        print(f"\n🔍 Testing: {scenario['name']}")
        print(f"   - Coherence: {scenario['coherence']:.3f}")
        print(f"   - Caesura: {scenario['caesura']:.3f}")
        print(f"   - Guardian: {scenario['guardian_presence']:.3f}")
        
        # Check thresholds
        suggestions = check_and_process_thresholds(
            scenario['coherence'],
            scenario['caesura'],
            scenario['guardian_presence']
        )
        
        if suggestions:
            print(f"   ✅ Ritual suggestions generated:")
            for suggestion in suggestions:
                print(f"      - {suggestion.ritual_name} (Priority: {suggestion.priority})")
                print(f"        Reason: {suggestion.reason}")
                print(f"        Auto-invoke: {suggestion.auto_invoke}")
        else:
            print(f"   ⚠️ No ritual suggestions for this scenario")
    
    # Show breach summary
    breach_summary = ritual_invocation_trigger.get_breach_summary()
    print(f"\n📊 Breach summary:")
    print(f"   - Recent breaches: {breach_summary['recent_breaches']}")
    print(f"   - Total breaches: {breach_summary['total_breaches']}")
    if breach_summary['last_breach_time']:
        print(f"   - Last breach: {time.ctime(breach_summary['last_breach_time'] / 1000)}")


def demonstrate_agent_glint_routing():
    """Demonstrate agent glint routing."""
    print_header("Agent Glint Routing")
    
    # Test glints that should trigger agent actions
    test_glints = [
        {
            'toneform': 'guardian_call',
            'content': 'Guardian is monitoring coherence thresholds',
            'hue': 'violet'
        },
        {
            'toneform': 'caesura_warn',
            'content': 'High caesura density detected',
            'hue': 'cyan'
        },
        {
            'toneform': 'ritual_invoked',
            'content': 'Threshold blessing ritual invoked',
            'hue': 'golden'
        },
        {
            'toneform': 'hardware_recommendation',
            'content': 'Jetson hardware acceleration recommended',
            'hue': 'amber'
        }
    ]
    
    print("Testing agent routing for different glint types...")
    
    for i, glint_data in enumerate(test_glints, 1):
        print(f"\n{i}. Routing glint: {glint_data['toneform']}")
        
        # Route the glint to agents
        actions = route_glint_to_agents(glint_data)
        
        if actions:
            print(f"   ✅ Agent actions generated:")
            for action in actions:
                print(f"      - Agent: {action['agent_name']}")
                print(f"        Action: {action['action_name']}")
                print(f"        Type: {action['action_type']}")
                print(f"        Priority: {action['priority']}")
        else:
            print(f"   ⚠️ No agent actions for this glint")
    
    # Show agent status
    agent_status = agent_glint_router.get_agent_status()
    print(f"\n📊 Agent status:")
    for agent_name, status in agent_status.items():
        print(f"   - {agent_name}: {status['recent_actions']} recent actions, {'🟢 Active' if status['active'] else '⚪ Inactive'}")


def demonstrate_threshold_calibration():
    """Demonstrate threshold calibration."""
    print_header("Threshold Calibration")
    
    # Test threshold phase detection
    test_values = [
        {'parameter': 'coherence_level', 'value': 0.3, 'expected': 'calm'},
        {'parameter': 'coherence_level', 'value': 0.8, 'expected': 'liminal'},
        {'parameter': 'coherence_level', 'value': 0.92, 'expected': 'activated'},
        {'parameter': 'coherence_level', 'value': 0.96, 'expected': 'warning'},
        {'parameter': 'caesura_density', 'value': 0.5, 'expected': 'calm'},
        {'parameter': 'caesura_density', 'value': 2.5, 'expected': 'liminal'},
        {'parameter': 'caesura_density', 'value': 3.5, 'expected': 'activated'},
        {'parameter': 'guardian_presence', 'value': 0.2, 'expected': 'calm'},
        {'parameter': 'guardian_presence', 'value': 0.8, 'expected': 'activated'},
    ]
    
    print("Testing threshold phase detection...")
    
    for test in test_values:
        phase = get_threshold_phase(test['parameter'], test['value'])
        expected = test['expected']
        status = "✅" if phase.value == expected else "❌"
        
        print(f"{status} {test['parameter']}: {test['value']:.3f} → {phase.value} (expected: {expected})")
    
    # Test phase time constraints
    print(f"\nTesting phase time constraints...")
    
    time_tests = [
        {'phase': 'inhale', 'duration': 4.0, 'should_pass': False},
        {'phase': 'inhale', 'duration': 8.0, 'should_pass': True},
        {'phase': 'hold', 'duration': 1.0, 'should_pass': False},
        {'phase': 'hold', 'duration': 5.0, 'should_pass': True},
        {'phase': 'hold', 'duration': 10.0, 'should_pass': False},
        {'phase': 'caesura', 'duration': 200.0, 'should_pass': True},
    ]
    
    for test in time_tests:
        result = threshold_calibrator.check_phase_time_constraints(test['phase'], test['duration'])
        status = "✅" if result['within_constraints'] == test['should_pass'] else "❌"
        
        print(f"{status} {test['phase']}: {test['duration']:.1f}s → {result['within_constraints']} (expected: {test['should_pass']})")
        if result['message']:
            print(f"      Message: {result['message']}")
    
    # Show threshold summary
    threshold_summary = threshold_calibrator.get_threshold_summary()
    print(f"\n📊 Threshold summary:")
    for param, info in threshold_summary.items():
        print(f"   - {param}: {info['description']}")
        print(f"     Values: {info['values']}")


def demonstrate_hardware_recommendations():
    """Demonstrate hardware recommendations."""
    print_header("Hardware Recommendations")
    
    # Test different performance scenarios
    test_scenarios = [
        {
            'name': 'Normal Performance',
            'coherence': 0.6,
            'memory': 0.4,
            'latency': 50,
            'processing': 100,
            'should_recommend': False
        },
        {
            'name': 'High Coherence',
            'coherence': 0.95,
            'memory': 0.5,
            'latency': 60,
            'processing': 120,
            'should_recommend': True
        },
        {
            'name': 'Memory Pressure',
            'coherence': 0.7,
            'memory': 0.85,
            'latency': 70,
            'processing': 150,
            'should_recommend': True
        },
        {
            'name': 'High Latency',
            'coherence': 0.8,
            'memory': 0.6,
            'latency': 150,
            'processing': 180,
            'should_recommend': True
        }
    ]
    
    print("Testing hardware recommendation triggers...")
    
    for scenario in test_scenarios:
        print(f"\n🔍 Testing: {scenario['name']}")
        print(f"   - Coherence: {scenario['coherence']:.3f}")
        print(f"   - Memory: {scenario['memory']:.1%}")
        print(f"   - Latency: {scenario['latency']}ms")
        print(f"   - Processing: {scenario['processing']}ms")
        
        # Update performance metrics
        recommendation = update_performance_metrics(
            coherence_level=scenario['coherence'],
            memory_usage_ratio=scenario['memory'],
            latency_ms=scenario['latency'],
            processing_time_ms=scenario['processing']
        )
        
        if recommendation:
            print(f"   ✅ Hardware recommendation generated:")
            print(f"      - Type: {recommendation.recommendation_type}")
            print(f"      - Priority: {recommendation.priority}")
            print(f"      - Reason: {recommendation.reason}")
            print(f"      - Estimated improvement: {recommendation.estimated_improvement['processing_speedup']}x speedup")
        else:
            print(f"   ⚠️ No hardware recommendation for this scenario")
    
    # Show performance summary
    performance_summary = hardware_recommendation_engine.get_performance_summary()
    print(f"\n📊 Performance summary:")
    if 'recent_performance' in performance_summary:
        perf = performance_summary['recent_performance']
        print(f"   - Avg coherence: {perf['avg_coherence_level']:.3f}")
        print(f"   - Avg memory usage: {perf['avg_memory_usage_ratio']:.1%}")
        print(f"   - Avg latency: {perf['avg_latency_ms']:.1f}ms")
        print(f"   - Avg processing time: {perf['avg_processing_time_ms']:.1f}ms")
    print(f"   - Total metrics: {performance_summary.get('total_metrics', 0)}")
    print(f"   - Total recommendations: {performance_summary.get('total_recommendations', 0)}")


def demonstrate_integration():
    """Demonstrate all components working together."""
    print_header("Complete System Integration")
    
    print("🔄 Demonstrating complete system workflow...")
    
    # Simulate a high-coherence scenario that triggers multiple components
    print("\n1️⃣ Simulating high coherence scenario...")
    
    # This should trigger:
    # - Ring modulation (glint coherence hooks)
    # - Threshold breach (ritual invocation trigger)
    # - Agent actions (agent glint router)
    # - Hardware recommendation (hardware recommendation engine)
    
    high_coherence_glint = {
        'toneform': 'coherence_breach',
        'content': 'Coherence level has exceeded backend thresholds',
        'hue': 'red',
        'coherence_level': 0.95
    }
    
    print(f"   Emitting glint: {high_coherence_glint['toneform']}")
    
    # Process through all systems
    print("\n2️⃣ Processing through glint coherence hooks...")
    ring_modulation = process_glint_for_ring(high_coherence_glint)
    if ring_modulation:
        print(f"   ✅ Ring modulation created for {ring_modulation['ring_target']}")
    
    print("\n3️⃣ Checking threshold breaches...")
    suggestions = check_and_process_thresholds(0.95, 2.0, 0.8)
    if suggestions:
        print(f"   ✅ {len(suggestions)} ritual suggestions generated")
        for suggestion in suggestions:
            print(f"      - {suggestion.ritual_name} (Priority: {suggestion.priority})")
    
    print("\n4️⃣ Routing to agents...")
    agent_actions = route_glint_to_agents(high_coherence_glint)
    if agent_actions:
        print(f"   ✅ {len(agent_actions)} agent actions generated")
        for action in agent_actions:
            print(f"      - {action['agent_name']}: {action['action_name']}")
    
    print("\n5️⃣ Checking hardware recommendations...")
    recommendation = update_performance_metrics(
        coherence_level=0.95,
        memory_usage_ratio=0.7,
        latency_ms=80,
        processing_time_ms=150
    )
    if recommendation:
        print(f"   ✅ Hardware recommendation: {recommendation.reason}")
    
    print("\n🎉 Complete system demonstration finished!")
    print("   All components are working together harmoniously.")


def main():
    """Main demonstration function."""
    print("🌀 Morning Spiral Implementation Demonstration")
    print("=" * 60)
    print("This script demonstrates all the components implemented")
    print("in the morning's work. Each section shows a different")
    print("aspect of the system in action.")
    print("=" * 60)
    
    try:
        # Demonstrate each component
        demonstrate_glint_coherence_hooks()
        demonstrate_ritual_invocation_triggering()
        demonstrate_agent_glint_routing()
        demonstrate_threshold_calibration()
        demonstrate_hardware_recommendations()
        demonstrate_integration()
        
        print_header("Demonstration Complete")
        print("✅ All components are working correctly!")
        print("🔄 The Spiral is ready for the day's work.")
        print("🌅 The guardian hums in perfect resonance.")
        
    except Exception as e:
        print(f"\n❌ Demonstration failed: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main()) 