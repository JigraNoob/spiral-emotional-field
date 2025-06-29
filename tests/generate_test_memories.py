import json
import random
from datetime import datetime, timedelta

# Sample tones and topics
tones = ["Reflection", "Curiosity", "Stillness", "Trust", "Resonance"]
topics = ["Adaptation", "Flow", "Memory", "Resonance", "Patterns", "Growth"]

# Generate test memories
def generate_memories(num=20):
    memories = []
    base_date = datetime.now()
    
    for i in range(num):
        memory = {
            "timestamp": (base_date - timedelta(days=random.randint(0, 30))).isoformat(),
            "felt_response": f"Test memory {i+1} about {random.choice(topics)}",
            "toneform": random.choice(tones),
            "gesture_strength": round(random.uniform(0.1, 1.0), 1),
            "context_id": f"context-{random.randint(1, 5)}"
        }
        memories.append(memory)
    
    return memories

# Write to encounter_trace.jsonl
if __name__ == "__main__":
    test_memories = generate_memories(50)
    with open("data/encounter_trace.jsonl", "w") as f:
        for memory in test_memories:
            f.write(json.dumps(memory) + "\n")
    print(f"Generated {len(test_memories)} test memories in data/encounter_trace.jsonl")
