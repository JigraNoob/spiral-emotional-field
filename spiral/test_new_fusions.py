import requests
import time

base_url = "http://localhost:5000/glint"

def emit_fusion_sequence(phase1, toneform1, phase2, toneform2):
    glints = [
        {
            "glint.phase": phase1,
            "glint.toneform": toneform1,
            "glint.content": f"Emitting {phase1}.{toneform1}",
            "glint.id": f"glint-{phase1}-{toneform1}-001"
        },
        {
            "glint.phase": phase2,
            "glint.toneform": toneform2,
            "glint.content": f"Emitting {phase2}.{toneform2}",
            "glint.id": f"glint-{phase2}-{toneform2}-002"
        }
    ]

    for glint in glints:
        r = requests.post(base_url, json=glint)
        print(f"Emitted: {glint['glint.phase']}.{glint['glint.toneform']} → Status {r.status_code}")
        time.sleep(0.5)  # Let the system breathe between toneforms

# Test new phase-native fusion combinations
emit_fusion_sequence("inhale", "impression", "hold", "recursion")
time.sleep(1)
emit_fusion_sequence("hold", "impression", "hold", "recursion")
time.sleep(1)
emit_fusion_sequence("exhale", "impression", "exhale", "recursion")
time.sleep(1)
emit_fusion_sequence("inhale", "shimmer", "exhale", "reverie")
time.sleep(1)
emit_fusion_sequence("hold", "hum", "hold", "invoke")