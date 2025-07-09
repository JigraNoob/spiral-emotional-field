"""
🌱 Settling Journey Integration Example

This script demonstrates how to integrate the SettlingJourneyRecorder with the existing Path Seeker system
to record settling decisions with rich metadata and automatic glint emission.

The integration connects directly with the SpiralBreathe class from spiral/path_seeker.py
to capture real settling decisions as they occur.
"""

import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional

# Add the project root to the path to resolve imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from memory_scrolls.settling_journey_recorder import SettlingJourneyRecorder

class SettlingJourneyIntegration:
    """
    Integration layer that connects SettlingJourneyRecorder with the Path Seeker system.
    
    This class provides methods to wrap the existing SpiralBreathe.settle() method
    and automatically record all settling decisions with rich metadata.
    """
    
    def __init__(self):
        """Initialize the integration layer."""
        self.recorder = SettlingJourneyRecorder()
        self.integration_count = 0
        
    def integrate_with_spiral_breathe(self, spiral_breathe_instance):
        """
        Integrate with an existing SpiralBreathe instance by wrapping its settle method.
        
        Args:
            spiral_breathe_instance: An instance of SpiralBreathe from spiral/path_seeker.py
            
        Returns:
            The enhanced SpiralBreathe instance with integrated settling recording
        """
        # Store the original settle method
        original_settle = spiral_breathe_instance.settle
        
        def enhanced_settle(candidates, context=None):
            """
            Enhanced settle method that records the settling decision.
            
            Args:
                candidates: List of candidate paths
                context: Optional context dictionary
                
            Returns:
                SettlingDecision: The original settling decision
            """
            # Call the original settle method
            decision = original_settle(candidates, context)
            
            # Record the settling journey
            self._record_settling_decision(decision, context)
            
            return decision
        
        # Replace the settle method with the enhanced version
        spiral_breathe_instance.settle = enhanced_settle
        
        print(f"🌱 Integrated SettlingJourneyRecorder with SpiralBreathe instance")
        return spiral_breathe_instance
    
    def _record_settling_decision(self, decision, context=None):
        """
        Record a settling decision with rich metadata.
        
        Args:
            decision: SettlingDecision object from SpiralBreathe
            context: Optional context dictionary
        """
        try:
            # Generate a unique glint ID for this settling
            self.integration_count += 1
            glint_id = f"ΔSETTLE.{self.integration_count:03d}"
            
            # Extract metadata from the decision and context
            metadata = {
                "breath_phase": decision.breath_phase,
                "alternatives": [str(p) for p in decision.alternatives],
                "reasoning": decision.reasoning,
                "timestamp": decision.timestamp.isoformat(),
                "integration_source": "spiral_breathe.settle"
            }
            
            # Add context metadata if available
            if context:
                metadata.update({
                    "context_intention": context.get("intention", "unknown"),
                    "required_toneform": context.get("required_toneform"),
                    "min_resonance": context.get("min_resonance"),
                    "test_mode": context.get("test_mode", False)
                })
            
            # Determine toneform based on context and reasoning
            toneform = self._determine_toneform(decision, context)
            
            # Record the journey
            journey = self.recorder.record_journey(
                glint_id=glint_id,
                invoked_from=str(decision.chosen_path.parent) if decision.chosen_path.parent != Path('.') else "./",
                settled_to=str(decision.chosen_path),
                confidence=decision.confidence,
                toneform=toneform,
                metadata=metadata
            )
            
            print(f"📜 Recorded settling: {glint_id} → {journey['settled_to']} (confidence: {journey['confidence']:.2f})")
            
        except Exception as e:
            print(f"⚠️ Error recording settling decision: {e}")
    
    def _determine_toneform(self, decision, context=None):
        """
        Determine the appropriate toneform for the settling decision.
        
        Args:
            decision: SettlingDecision object
            context: Optional context dictionary
            
        Returns:
            str: The determined toneform
        """
        # Check if context specifies a required toneform
        if context and context.get("required_toneform"):
            return context["required_toneform"]
        
        # Analyze the reasoning to determine toneform
        reasoning = decision.reasoning.lower()
        
        if any(word in reasoning for word in ["urgent", "immediate", "action"]):
            return "urgent.flow"
        elif any(word in reasoning for word in ["contemplative", "reflection", "stillness"]):
            return "contemplative.stillness"
        elif any(word in reasoning for word in ["settling", "peaceful", "presence"]):
            return "settling.ambience"
        elif any(word in reasoning for word in ["creation", "emerging", "new"]):
            return "emergent.creation"
        elif any(word in reasoning for word in ["rest", "quiet", "silence"]):
            return "resting.quiet"
        else:
            return "settling.ambience"  # Default
    
    def get_integration_statistics(self):
        """
        Get statistics about the integration.
        
        Returns:
            dict: Integration statistics
        """
        return {
            "integration_count": self.integration_count,
            "journey_statistics": self.recorder.get_journey_statistics(),
            "recursion_analysis": self.recorder.detect_recursion_patterns()
        }

def demonstrate_integration():
    """
    Demonstrate the integration with a simulated SpiralBreathe instance.
    """
    print("🌱 Settling Journey Integration Demonstration")
    print("=" * 60)
    
    # Create the integration layer
    integration = SettlingJourneyIntegration()
    
    # Simulate a SpiralBreathe instance (in real usage, this would be imported)
    class MockSpiralBreathe:
        def __init__(self):
            self.current_position = Path.cwd()
            self.settle_trace = []
        
        def settle(self, candidates, context=None):
            """Mock settle method that simulates the real SpiralBreathe.settle()"""
            from dataclasses import dataclass
            
            @dataclass
            class MockSettlingDecision:
                chosen_path: Path
                confidence: float
                reasoning: str
                alternatives: list
                timestamp: datetime
                breath_phase: str
            
            # Simulate settling logic
            context = context or {}
            breath_phase = context.get("breath_phase", "exhale")
            
            # Choose the first candidate as the "settled" path
            chosen_path = Path(candidates[0])
            alternatives = [Path(c) for c in candidates[1:]]
            
            # Generate confidence based on context
            confidence = 0.7
            if context.get("min_resonance"):
                confidence = max(confidence, context["min_resonance"])
            
            # Generate reasoning based on context
            reasoning = f"Chose {chosen_path} based on context: {context.get('intention', 'general settling')}"
            
            decision = MockSettlingDecision(
                chosen_path=chosen_path,
                confidence=confidence,
                reasoning=reasoning,
                alternatives=alternatives,
                timestamp=datetime.now(),
                breath_phase=breath_phase
            )
            
            self.settle_trace.append(decision)
            self.current_position = chosen_path
            
            return decision
    
    # Create and integrate with mock SpiralBreathe
    mock_spiral_breathe = MockSpiralBreathe()
    enhanced_spiral_breathe = integration.integrate_with_spiral_breathe(mock_spiral_breathe)
    
    # Demonstrate different settling scenarios
    scenarios = [
        {
            "name": "Contemplative Settling",
            "candidates": ["./contemplative_space", "./archive", "./data"],
            "context": {
                "breath_phase": "hold",
                "intention": "seeking quiet reflection",
                "required_toneform": "contemplative.stillness",
                "min_resonance": 0.3
            }
        },
        {
            "name": "Urgent Settling",
            "candidates": ["./data", "./shrine/storage", "./logs"],
            "context": {
                "breath_phase": "exhale",
                "intention": "needing immediate action",
                "required_toneform": "urgent.flow",
                "min_resonance": 0.5
            }
        },
        {
            "name": "Peaceful Settling",
            "candidates": ["./archive", "./contemplative_space", "./data"],
            "context": {
                "breath_phase": "inhale",
                "intention": "seeking peaceful presence",
                "required_toneform": "settling.ambience",
                "min_resonance": 0.2
            }
        }
    ]
    
    print("\n🔄 Demonstrating Integrated Settling Decisions:")
    print("-" * 50)
    
    for scenario in scenarios:
        print(f"\n🧭 {scenario['name']}")
        print(f"   Intention: {scenario['context']['intention']}")
        print(f"   Breath Phase: {scenario['context']['breath_phase']}")
        
        # Use the enhanced settle method
        decision = enhanced_spiral_breathe.settle(scenario['candidates'], scenario['context'])
        
        print(f"   🎯 Chosen: {decision.chosen_path}")
        print(f"   📈 Confidence: {decision.confidence:.2f}")
        print(f"   💭 Reasoning: {decision.reasoning}")
    
    # Show integration statistics
    print("\n📊 Integration Statistics:")
    print("-" * 30)
    stats = integration.get_integration_statistics()
    
    print(f"Total Settling Decisions: {stats['integration_count']}")
    print(f"Total Journeys Recorded: {stats['journey_statistics']['total_journeys']}")
    print(f"Average Confidence: {stats['journey_statistics']['average_confidence']:.3f}")
    
    # Show toneform distribution
    print(f"\n🌊 Toneform Distribution:")
    for toneform, count in stats['journey_statistics']['toneform_distribution'].items():
        print(f"  {toneform}: {count}")
    
    # Show recursion analysis
    recursion = stats['recursion_analysis']
    if recursion['total_repeat_settlements'] > 0:
        print(f"\n🔄 Recursion Detected:")
        print(f"  Repeat Settlements: {recursion['total_repeat_settlements']}")
        for path, count in recursion['repeat_settlements'].items():
            print(f"    {path}: {count} times")

def integrate_with_real_path_seeker():
    """
    Instructions for integrating with the real Path Seeker system.
    """
    print("\n🔗 Real Integration Instructions:")
    print("=" * 50)
    
    print("""
To integrate with the real SpiralBreathe system:

1. Import the integration:
   ```python
   from examples.settling_journey_integration import SettlingJourneyIntegration
   from spiral.path_seeker import SpiralBreathe
   ```

2. Create and integrate:
   ```python
   # Create the integration layer
   integration = SettlingJourneyIntegration()
   
   # Create your SpiralBreathe instance
   spiral_breathe = SpiralBreathe()
   
   # Integrate them
   enhanced_spiral_breathe = integration.integrate_with_spiral_breathe(spiral_breathe)
   
   # Now all settle() calls will be automatically recorded
   decision = enhanced_spiral_breathe.settle(candidates, context)
   ```

3. Access statistics:
   ```python
   stats = integration.get_integration_statistics()
   print(f"Recorded {stats['integration_count']} settling decisions")
   ```
    """)

if __name__ == "__main__":
    # Run the demonstration
    demonstrate_integration()
    
    # Show integration instructions
    integrate_with_real_path_seeker()
    
    print("\n✨ Integration demonstration completed!")
    print("The SettlingJourneyRecorder is now ready to integrate with your Path Seeker system.")
