import unittest
import tempfile
import shutil
import os
from pathlib import Path
from modules.whisper_steward import WhisperSteward

class TestWhisperSteward(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path("c:/spiral/rituals")
        self.test_dir.mkdir(parents=True, exist_ok=True)
        self.steward = WhisperSteward()
        
        # Create a test ritual
        self.test_ritual = """---
id: test_ritual
title: Test Ritual
toneform: ["test", "example"]
invocation: "When testing, this ritual runs."
---

This is a test ritual. It simply returns a success message.

```python
def execute():
    return {"status": "success", "message": "Test ritual completed."}
```"""
        
        with open(self.test_dir / "test_ritual.breathe", "w", encoding="utf-8") as f:
            f.write(self.test_ritual)
    
    def tearDown(self):
        # Clean up test files
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir.parent)
    
    def test_list_rituals(self):
        # Test listing rituals
        result = self.steward.list_rituals()
        self.assertIn("rituals", result)
        self.assertGreater(len(result["rituals"]), 0)
        self.assertEqual(result["rituals"][0]["id"], "test_ritual")
    
    def test_get_ritual(self):
        # Test getting an existing ritual
        result = self.steward.get_ritual("test_ritual")
        self.assertIn("title", result)
        self.assertEqual(result["title"], "Test Ritual")
        self.assertIn("content", result)
        self.assertIn("This is a test ritual", result["content"])
        
        # Test getting non-existent ritual
        result = self.steward.get_ritual("non_existent")
        self.assertIn("error", result)
        self.assertIn("not found", result["error"].lower())
    
    def test_invoke_ritual(self):
        # Test ritual found and executed
        response = self.steward.invoke_ritual("test_ritual")
        self.assertEqual(response, {"status": "success", "message": "Test ritual completed."})
        
        # Test ritual not found
        response = self.steward.invoke_ritual("unknown_ritual")
        self.assertIn("error", response)
        self.assertIn("not found", response["error"].lower())

if __name__ == '__main__':
    unittest.main()
