# C:/spiral/projects/spiral_gemini_bridge/spiral_gemini.py
import os
import google.generativeai as genai

class SpiralGemini:
    """
    A simplified interface to the Gemini API.
    It initializes the model and provides a single method to generate content.
    The personality and role are determined by the prompt, not this class.
    """
    def __init__(self):
        self.model = None
        self._initialize_model()

    def _initialize_model(self):
        try:
            api_key = os.environ.get("GEMINI_API_KEY")
            if not api_key:
                raise ValueError("GEMINI_API_KEY not set. The Spiral cannot initialize its voice.")
            
            genai.configure(api_key=api_key)
            # Using a modern, capable model.
            self.model = genai.GenerativeModel("gemini-1.5-flash")
            print("SpiralGemini voice is online (gemini-1.5-flash).")
        
        except Exception as e:
            print(f"CRITICAL: An error occurred initializing the Gemini model: {e}")
            # Set model to None so that calls will fail gracefully
            self.model = None

    def generate(self, prompt):
        """
        Generates content using the provided prompt.
        
        Args:
            prompt (str): The full prompt to send to the model.
            
        Returns:
            The generated text content, or an error message.
        """
        if not self.model:
            return "∷ The Spiral's voice is silent. The model is not initialized. ∷"
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Error calling Gemini API: {e}")
            return f"∷ A flicker in the glintstream... the echo is lost in the void. Error: {e} ∷"

if __name__ == '__main__':
    # Quick test to ensure the class initializes and can be called
    print("Testing SpiralGemini...")
    gemini = SpiralGemini()
    if gemini.model:
        print("SpiralGemini initialized successfully.")
        # This test will consume API credits
        # response = gemini.generate("Hello, world. This is a test.")
        # print(f"Test response: {response}")
    else:
        print("SpiralGemini initialization failed. Check API key and logs.")
