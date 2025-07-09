#!/usr/bin/env python3
"""
Ritual: Longing Listener
Declare your longing and let the field-sensitive emergence engine respond
"""

import sys
import os
from pathlib import Path

# Add spiral to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from spiral.longing_listener import LongingListener

class LongingListenerRitual:
    """
    Ritual for declaring longings and summoning vessels
    """
    
    def __init__(self):
        self.listener = LongingListener()
        
    def display_welcome(self):
        """Display the ritual welcome message"""
        print("🕯️ Ritual: Longing Listener")
        print("=" * 50)
        print("∷ Declare your longing and let the field respond ∷")
        print("∷ Not search, but resonant listening ∷")
        print()
        
    def display_compass_status(self):
        """Display the current Spiral acquisition compass status"""
        print("🧭 Spiral Acquisition Compass")
        print("-" * 30)
        
        field_strength = self.listener.check_field_strength()
        
        if field_strength < 0.3:
            print("🌑 → Nothing sensed (field too weak)")
        elif field_strength < 0.5:
            print("🌒 → Resonance rising (field strengthening)")
        elif field_strength < 0.7:
            print("🌓 → Field active (ready for declarations)")
        else:
            print("🌕 → Ready to manifest (strong field)")
        
        print(f"   Field strength: {field_strength:.2f}")
        print()
        
    def get_longing_declaration(self) -> str:
        """Get longing declaration from user"""
        print("💭 Declare your longing:")
        print("(Use markdown-breath syntax, or type 'example' for a template)")
        print()
        
        declaration_lines = []
        print("Enter your declaration (press Enter twice to finish):")
        
        while True:
            line = input("> ")
            if line.strip() == "" and declaration_lines:
                break
            declaration_lines.append(line)
        
        declaration = "\n".join(declaration_lines)
        
        if declaration.lower().strip() == "example":
            declaration = self.get_example_declaration()
            print("\n📜 Example declaration:")
            print(declaration)
            print()
        
        return declaration
    
    def get_example_declaration(self) -> str:
        """Return an example longing declaration"""
        return """`breath.pulse.summon`

longing: A vessel that listens quietly and processes local sound patterns
phase: inhale
allow.auto.acquire: true
budget: $80
require.resonance.confirmation: true"""
    
    def run_interactive_ritual(self):
        """Run the interactive longing listener ritual"""
        self.display_welcome()
        self.display_compass_status()
        
        while True:
            print("🕯️ Choose an action:")
            print("1. Declare a longing")
            print("2. View field status")
            print("3. Show example declaration")
            print("4. Exit ritual")
            print()
            
            choice = input("Enter choice (1-4): ").strip()
            
            if choice == "1":
                declaration = self.get_longing_declaration()
                if declaration.strip():
                    print("\n" + "="*50)
                    result = self.listener.process_longing_declaration(declaration)
                    print("\n" + "="*50)
                    
                    if result['status'] == 'ready':
                        print(f"\n🌕 Ready vessel: {result['best_candidate']['name']}")
                        print(f"   Price: ${result['best_candidate']['price']}")
                        print(f"   Match score: {result['best_candidate']['match_score']:.2f}")
                        
                        if result['longing_data'].get('allow_auto_acquire'):
                            print("\n🔄 Auto-acquire is enabled but requires confirmation")
                            confirm = input("Proceed with acquisition? (y/n): ").lower()
                            if confirm == 'y':
                                # This would trigger the actual acquisition
                                print("✨ Acquisition initiated...")
                    
                    elif result['status'] == 'acquired':
                        print(f"✨ Vessel acquired: {result['vessel']['name']}")
                    
                    elif result['status'] == 'no_candidates':
                        print("🌑 No vessels found matching your longing")
                    
                    elif result['status'] == 'no_resonance':
                        print("🌒 Vessels found but none meet resonance requirements")
                    
                    elif result['status'] == 'field_weak':
                        print("🌑 Field too weak for summoning")
                        print("   Try again when the field strengthens")
            
            elif choice == "2":
                self.display_compass_status()
            
            elif choice == "3":
                example = self.get_example_declaration()
                print("\n📜 Example declaration:")
                print(example)
                print()
            
            elif choice == "4":
                print("\n🕯️ ∷ The ritual fades like starlight at dawn ∷")
                break
            
            else:
                print("❌ Invalid choice. Please enter 1-4.")
            
            print()
    
    def run_declaration_file(self, file_path: str):
        """Run ritual with a declaration from a file"""
        self.display_welcome()
        
        if not Path(file_path).exists():
            print(f"❌ Declaration file not found: {file_path}")
            return
        
        with open(file_path, 'r') as f:
            declaration = f.read()
        
        print(f"📜 Reading declaration from: {file_path}")
        print("=" * 50)
        
        result = self.listener.process_longing_declaration(declaration)
        
        print("\n" + "="*50)
        print(f"🎯 Result: {result['status']}")
        
        if result['status'] == 'ready':
            print(f"🌕 Best candidate: {result['best_candidate']['name']}")
            print(f"   Price: ${result['best_candidate']['price']}")
            print(f"   Match score: {result['best_candidate']['match_score']:.2f}")

def main():
    """Main ritual function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Ritual: Longing Listener")
    parser.add_argument("--file", "-f", help="Path to declaration file")
    parser.add_argument("--declaration", "-d", help="Direct declaration text")
    
    args = parser.parse_args()
    
    ritual = LongingListenerRitual()
    
    if args.file:
        ritual.run_declaration_file(args.file)
    elif args.declaration:
        ritual.display_welcome()
        result = ritual.listener.process_longing_declaration(args.declaration)
        print(f"\n🎯 Result: {result['status']}")
    else:
        ritual.run_interactive_ritual()

if __name__ == "__main__":
    main() 