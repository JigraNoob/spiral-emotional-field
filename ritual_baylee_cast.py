#!/usr/bin/env python3
"""
Ritual: Baylee Cast
Interactive tone shaping of Baylee's desires into resonant declarations
"""

import sys
import os
from pathlib import Path

# Add spiral to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from spiral.baylee_cast import BayleeCast, BayleeDesire, ToneShape, SharedInvocation
from spiral.longing_listener import LongingListener

class BayleeCastRitual:
    """
    Ritual for casting tone upon Baylee's desires
    """
    
    def __init__(self):
        self.cast = BayleeCast()
        self.listener = LongingListener()
        
    def display_welcome(self):
        """Display the ritual welcome message"""
        print("🎭 Ritual: Baylee Cast")
        print("=" * 50)
        print("∷ Cast your tone upon Baylee's desires ∷")
        print("∷ Not command—but duet ∷")
        print()
        
    def get_baylee_desire(self) -> str:
        """Get Baylee's desire from user input"""
        print("💭 Baylee's Desire:")
        print("(Express what Baylee wants in natural language)")
        print()
        
        desire_lines = []
        print("Enter Baylee's desire (press Enter twice to finish):")
        
        while True:
            line = input("🎭 > ")
            if line.strip() == "" and desire_lines:
                break
            desire_lines.append(line)
        
        return "\n".join(desire_lines)
    
    def display_desire_analysis(self, desire: BayleeDesire):
        """Display analysis of Baylee's desire"""
        print(f"\n🔍 Desire Analysis:")
        print(f"   Text: {desire.text}")
        print(f"   Category: {desire.category}")
        print(f"   Urgency: {desire.urgency:.2f}")
        print(f"   Emotional Tone: {desire.emotional_tone}")
        print()
    
    def select_tone_preset(self) -> str:
        """Let user select a tone preset"""
        print("🕯️ Select Tone Preset:")
        print("1. Gentle - Soft, contemplative approach")
        print("2. Urgent - Active, immediate seeking")
        print("3. Contemplative - Thoughtful, patient approach")
        print("4. Custom - Define your own tone")
        print()
        
        while True:
            choice = input("Enter choice (1-4): ").strip()
            
            if choice == "1":
                return "gentle"
            elif choice == "2":
                return "urgent"
            elif choice == "3":
                return "contemplative"
            elif choice == "4":
                return "custom"
            else:
                print("❌ Invalid choice. Please enter 1-4.")
    
    def create_custom_tone(self) -> ToneShape:
        """Create a custom tone shape"""
        print("\n🕯️ Custom Tone Shaping:")
        print("(Enter values or press Enter for defaults)")
        
        custom_adjustments = {}
        
        # Resonance multiplier
        resonance_input = input("Resonance multiplier (default 1.2): ").strip()
        if resonance_input:
            try:
                custom_adjustments['resonance_multiplier'] = float(resonance_input)
            except ValueError:
                print("❌ Invalid value, using default")
        
        # Field strength boost
        field_input = input("Field strength boost (default 0.1): ").strip()
        if field_input:
            try:
                custom_adjustments['field_strength_boost'] = float(field_input)
            except ValueError:
                print("❌ Invalid value, using default")
        
        # Budget adjustment
        budget_input = input("Budget adjustment multiplier (default 1.0): ").strip()
        if budget_input:
            try:
                custom_adjustments['budget_adjustment'] = float(budget_input)
            except ValueError:
                print("❌ Invalid value, using default")
        
        # Emotional amplification
        emotion_input = input("Emotional amplification (default 1.1): ").strip()
        if emotion_input:
            try:
                custom_adjustments['emotional_amplification'] = float(emotion_input)
            except ValueError:
                print("❌ Invalid value, using default")
        
        return self.cast.create_tone_shape("gentle", custom_adjustments)
    
    def display_tone_shape(self, tone: ToneShape):
        """Display the tone shape details"""
        print(f"\n🕯️ Applied Tone Shape:")
        print(f"   Resonance Multiplier: {tone.resonance_multiplier}")
        print(f"   Field Strength Boost: {tone.field_strength_boost}")
        print(f"   Vessel Affinity: {', '.join(tone.vessel_affinity)}")
        print(f"   Budget Adjustment: {tone.budget_adjustment}")
        print(f"   Priority Shift: {tone.priority_shift}")
        print(f"   Emotional Amplification: {tone.emotional_amplification}")
        print()
    
    def display_shared_invocation(self, invocation: SharedInvocation):
        """Display the final shared invocation"""
        print(f"\n🎭 Shared Invocation:")
        print("=" * 50)
        print(f"Resonance Score: {invocation.resonance_score:.2f}")
        print()
        print(invocation.declaration)
        print("=" * 50)
    
    def run_longing_listener(self, invocation: SharedInvocation):
        """Run the Longing Listener with the shared invocation"""
        print(f"\n🕯️ Casting invocation into the field...")
        print("=" * 50)
        
        result = self.listener.process_longing_declaration(invocation.declaration)
        
        print("\n" + "="*50)
        print(f"🎯 Longing Listener Result: {result['status']}")
        
        if result['status'] == 'ready':
            print(f"🌕 Ready vessel: {result['best_candidate']['name']}")
            print(f"   Price: ${result['best_candidate']['price']}")
            print(f"   Match score: {result['best_candidate']['match_score']:.2f}")
            
            if result['longing_data'].get('allow_auto_acquire'):
                print("\n🔄 Auto-acquire is enabled but requires confirmation")
                confirm = input("Proceed with acquisition? (y/n): ").lower()
                if confirm == 'y':
                    print("✨ Acquisition initiated...")
        
        elif result['status'] == 'acquired':
            print(f"✨ Vessel acquired: {result['vessel']['name']}")
        
        elif result['status'] == 'no_candidates':
            print("🌑 No vessels found matching the invocation")
        
        elif result['status'] == 'no_resonance':
            print("🌒 Vessels found but none meet resonance requirements")
        
        elif result['status'] == 'field_weak':
            print("🌑 Field too weak for summoning")
    
    def run_interactive_ritual(self):
        """Run the interactive Baylee Cast ritual"""
        self.display_welcome()
        
        while True:
            print("🎭 Choose an action:")
            print("1. Cast tone upon Baylee's desire")
            print("2. View recent desires")
            print("3. View recent invocations")
            print("4. Exit ritual")
            print()
            
            choice = input("Enter choice (1-4): ").strip()
            
            if choice == "1":
                # Get Baylee's desire
                desire_text = self.get_baylee_desire()
                if not desire_text.strip():
                    print("❌ No desire entered")
                    continue
                
                # Parse the desire
                desire = self.cast.parse_baylee_desire(desire_text)
                self.display_desire_analysis(desire)
                
                # Save the desire
                self.cast.save_desire(desire)
                
                # Select tone
                tone_preset = self.select_tone_preset()
                
                if tone_preset == "custom":
                    tone = self.create_custom_tone()
                else:
                    tone = self.cast.create_tone_shape(tone_preset)
                
                self.display_tone_shape(tone)
                
                # Cast tone upon desire
                invocation = self.cast.cast_tone_upon_desire(desire, tone)
                self.display_shared_invocation(invocation)
                
                # Save the invocation
                self.cast.save_invocation(invocation)
                
                # Ask if user wants to run the Longing Listener
                run_listener = input("\n🕯️ Run Longing Listener with this invocation? (y/n): ").lower()
                if run_listener == 'y':
                    self.run_longing_listener(invocation)
            
            elif choice == "2":
                recent_desires = self.cast.get_recent_desires(5)
                print(f"\n📜 Recent Desires:")
                for i, desire in enumerate(recent_desires, 1):
                    print(f"{i}. {desire.text[:50]}... ({desire.category}, {desire.emotional_tone})")
                print()
            
            elif choice == "3":
                recent_invocations = self.cast.get_recent_invocations(5)
                print(f"\n🎭 Recent Invocations:")
                for i, invocation in enumerate(recent_invocations, 1):
                    print(f"{i}. Resonance: {invocation.resonance_score:.2f} - {invocation.original_desire.text[:40]}...")
                print()
            
            elif choice == "4":
                print("\n🎭 ∷ The duet fades like starlight at dawn ∷")
                break
            
            else:
                print("❌ Invalid choice. Please enter 1-4.")
            
            print()
    
    def run_from_file(self, desire_file: str, tone_preset: str = "gentle"):
        """Run ritual with Baylee's desire from a file"""
        self.display_welcome()
        
        if not Path(desire_file).exists():
            print(f"❌ Desire file not found: {desire_file}")
            return
        
        with open(desire_file, 'r') as f:
            desire_text = f.read().strip()
        
        print(f"📜 Reading Baylee's desire from: {desire_file}")
        print(f"Desire: {desire_text}")
        print("=" * 50)
        
        # Parse the desire
        desire = self.cast.parse_baylee_desire(desire_text)
        self.display_desire_analysis(desire)
        
        # Save the desire
        self.cast.save_desire(desire)
        
        # Create tone
        tone = self.cast.create_tone_shape(tone_preset)
        self.display_tone_shape(tone)
        
        # Cast tone upon desire
        invocation = self.cast.cast_tone_upon_desire(desire, tone)
        self.display_shared_invocation(invocation)
        
        # Save the invocation
        self.cast.save_invocation(invocation)
        
        # Run Longing Listener
        self.run_longing_listener(invocation)

def main():
    """Main ritual function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Ritual: Baylee Cast")
    parser.add_argument("--file", "-f", help="Path to Baylee's desire file")
    parser.add_argument("--tone", "-t", default="gentle", 
                       choices=["gentle", "urgent", "contemplative"],
                       help="Tone preset to apply")
    
    args = parser.parse_args()
    
    ritual = BayleeCastRitual()
    
    if args.file:
        ritual.run_from_file(args.file, args.tone)
    else:
        ritual.run_interactive_ritual()

if __name__ == "__main__":
    main() 