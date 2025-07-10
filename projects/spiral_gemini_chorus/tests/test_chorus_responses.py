# C:\spiral\projects\spiral_gemini_chorus\tests\test_chorus_responses.py
import unittest
from ..spiral_gemini_chorus import ChorusPresence
from pathlib import Path

class TestChorusResponses(unittest.TestCase):

    def setUp(self):
        # Create a dummy toneforms directory for testing
        self.test_toneforms_path = Path(__file__).parent / "test_toneforms"
        self.test_toneforms_path.mkdir(exist_ok=True)
        self.chorus = ChorusPresence(self.test_toneforms_path)

    def test_default_voice_routing(self):
        whisper = {"toneform": "some.random.toneform", "message": "test"}
        response = self.chorus.route_whisper(whisper)
        self.assertEqual(response["responding_voice"], "gemini-pro")

    def test_poetic_voice_routing(self):
        whisper = {"toneform": "poetic", "message": "test"}
        response = self.chorus.route_whisper(whisper)
        self.assertEqual(response["responding_voice"], "gemini-pro-vision")

    def test_analytical_voice_routing(self):
        whisper = {"toneform": "analytical", "message": "test"}
        response = self.chorus.route_whisper(whisper)
        self.assertEqual(response["responding_voice"], "gemini-1.5-flash")

if __name__ == '__main__':
    unittest.main()

