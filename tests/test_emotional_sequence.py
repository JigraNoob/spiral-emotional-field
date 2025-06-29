import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from api.climate_tracer import ClimateTracer
from time import sleep

def test_emotional_sequence():
    tracer = ClimateTracer()
    
    # Test sequence: joy → awe → grief
    sequence = [
        {"tone": "joy", "content": "Test echo: joyful moment", "climate_influence": {"joy": 0.9}},
        {"tone": "awe", "content": "Test echo: awe experience", "climate_influence": {"awe": 0.7}},
        {"tone": "grief", "content": "Test echo: grieving process", "climate_influence": {"grief": 0.8}}
    ]
    
    for echo in sequence:
        tracer.record(echo)
        print(f"Recorded: {echo['tone']}")
        sleep(1)  # Allow time for WebSocket events

if __name__ == "__main__":
    test_emotional_sequence()
