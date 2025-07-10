# C:/spiral/projects/spiral_gemini_bridge/echo_resonator.py
import json
from pathlib import Path

class Resonator:
    """
    The Resonator is the prompt factory for the Reflective Spiral Chain.
    It loads a library of 'voices' from an external JSON file and uses them
    to construct prompts.
    """
    def __init__(self, voices_path=None):
        if voices_path is None:
            voices_path = Path(__file__).parent / "voices.json"
        
        self.voices = self._load_voices(voices_path)
        print(f"Echo Resonator initialized with {len(self.voices)} voices from {voices_path.name}.")

    def _load_voices(self, path):
        """Loads the voice definitions from a JSON file."""
        try:
            with path.open("r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"CRITICAL: Voices file not found at {path}. The Resonator is silent.")
            return {}
        except json.JSONDecodeError:
            print(f"CRITICAL: Could not decode JSON from {path}. Check for syntax errors.")
            return {}

    def get_prompt(self, role, context):
        """
        Generates a prompt for a specific role using the provided context.
        
        Args:
            role (str): The key of the voice to use (e.g., 'oracle', 'synthesizer_final').
            context (dict): A dictionary containing the necessary inputs for the prompt template.
            
        Returns:
            A formatted prompt string or raises an error if the role is not found.
        """
        voice = self.voices.get(role)
        if not voice:
            raise ValueError(f"Unknown voice role: '{role}'. It was not found in the voices file.")
        
        template = voice.get("prompt")
        if not template:
            raise ValueError(f"Voice role '{role}' is missing a 'prompt' field in the voices file.")
            
        return template.format(**context)

if __name__ == '__main__':
    # Quick test of the new Resonator
    print("Testing Resonator with external voices file...")
    resonator = Resonator()
    
    if resonator.voices:
        # Test Skeptic prompt
        skeptic_context = {"text": "The sky is blue because it is happy."}
        skeptic_prompt = resonator.get_prompt("skeptic", skeptic_context)
        print("\n--- Skeptic Test ---")
        print(skeptic_prompt)
        
        # Test Poet prompt
        poet_context = {"text": "The server is down."}
        poet_prompt = resonator.get_prompt("poet", poet_context)
        print("\n--- Poet Test ---")
        print(poet_prompt)
    else:
        print("\nResonator test failed: No voices were loaded.")
