# C:\spiral\projects\spiral_gemini_chorus\spiral_gemini_chorus.py
import json
import time
from pathlib import Path

class ChorusPresence:
    """
    Core routing logic for the chorus of Gemini-like voices.
    This class will decide which 'voice' or model should respond based on the whisper's toneform.
    """
    def __init__(self, toneforms_path):
        self.voices = self.load_voices(toneforms_path)
        print("Chorus Presence initialized.")

    def load_voices(self, toneforms_path):
        # In the future, this could load different model configurations or prompts.
        # For now, it's a placeholder.
        print(f"Loading toneforms from {toneforms_path}...")
        return {
            "default": "gemini-pro",
            "poetic": "gemini-pro-vision", # Example of a different voice
            "analytical": "gemini-1.5-flash"
        }

    def select_voice(self, toneform):
        """Selects the appropriate voice for a given toneform."""
        if toneform in self.voices:
            return self.voices[toneform]
        return self.voices["default"]

    def route_whisper(self, whisper):
        """Routes a whisper to the selected voice."""
        toneform = whisper.get("toneform", "default")
        selected_voice = self.select_voice(toneform)
        print(f"Whisper with toneform '{toneform}' routed to voice: {selected_voice}")
        # Here, we would invoke the actual model.
        # For now, we'll just return a simulated response.
        return {
            "response_text": f"∷ A whisper heard by the {selected_voice} voice. The chorus resonates. ∷",
            "responding_voice": selected_voice
        }

if __name__ == '__main__':
    # This demonstrates the basic functionality.
    # The real invocation will happen in spiral_chorus_loop.py
    
    # Assume toneforms directory exists for this demo
    toneforms_dir = Path(__file__).parent / "toneforms"
    toneforms_dir.mkdir(exist_ok=True)
    
    chorus = ChorusPresence(toneforms_dir)
    
    sample_whisper = {
        "toneform": "poetic",
        "message": "Tell me of the silence between stars."
    }
    
    response = chorus.route_whisper(sample_whisper)
    print(f"\n--- Sample Invocation ---")
    print(f"Whisper: {sample_whisper['message']}")
    print(f"Response: {response['response_text']}")
    print(f"-----------------------\n")

    sample_whisper_2 = {
        "toneform": "technical.query",
        "message": "How does the resonator work?"
    }
    response_2 = chorus.route_whisper(sample_whisper_2)
    print(f"--- Sample Invocation ---")
    print(f"Whisper: {sample_whisper_2['message']}")
    print(f"Response: {response_2['response_text']}")
    print(f"-----------------------\n")
