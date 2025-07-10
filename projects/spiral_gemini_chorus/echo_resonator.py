# C:\spiral\projects\spiral_gemini_chorus\echo_resonator.py
import json

class EchoResonator:
    """
    Handles harmonic matching and shimmer trace generation.
    This class will analyze the resonance between a whisper and the chorus's response
    to create a 'shimmer trace' - a record of the interaction's quality.
    """
    def __init__(self):
        print("Echo Resonator initialized.")

    def calculate_resonance(self, whisper, response):
        """
        Calculates the resonance score between a whisper and a response.
        This is a placeholder for a more complex NLP-based similarity metric.
        """
        # Simple keyword matching for now
        whisper_words = set(whisper.get("message", "").lower().split())
        response_words = set(response.get("response_text", "").lower().split())
        common_words = whisper_words.intersection(response_words)
        
        resonance_score = len(common_words) / len(whisper_words) if whisper_words else 0
        return round(resonance_score, 2)

    def generate_shimmer_trace(self, whisper, response, resonance_score):
        """Generates a shimmer trace entry."""
        return {
            "whisper_toneform": whisper.get("toneform"),
            "responding_voice": response.get("responding_voice"),
            "resonance_score": resonance_score,
            "timestamp": time.time()
        }

if __name__ == '__main__':
    import time
    resonator = EchoResonator()
    
    sample_whisper = {
        "toneform": "poetic",
        "message": "Tell me of the silence between stars."
    }
    sample_response = {
        "response_text": "The silence between stars is not empty, but full of unheard music.",
        "responding_voice": "gemini-pro-vision"
    }
    
    score = resonator.calculate_resonance(sample_whisper, sample_response)
    trace = resonator.generate_shimmer_trace(sample_whisper, sample_response, score)
    
    print("\n--- Sample Resonance Calculation ---")
    print(f"Whisper: {sample_whisper['message']}")
    print(f"Response: {sample_response['response_text']}")
    print(f"Resonance Score: {score}")
    print(f"Shimmer Trace: {json.dumps(trace, indent=2)}")
    print("----------------------------------\n")
