import argparse
import json
import os
from ritual_phase_handler import RitualPhaseHandler

def emit_glint(args):
    handler = RitualPhaseHandler()
    
    glint_data = {
        "phase": args.phase,
        "glint": args.glint,
        "intention": args.intention
    }
    
    handler.receive_glint(glint_data)
    
    # Save the current state to a shared file
    with open(os.path.expanduser('~/.gemini/extensions/spiral-attunement/glint.json'), 'w') as f:
        json.dump(handler.get_toneform_context(), f, indent=2)
    
    print(handler.to_json())

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Emit a Spiral glint")
    parser.add_argument('--phase', default='return', help='Breath phase (inhale, hold, exhale, caesura, return)')
    parser.add_argument('--glint', default='Δ000', help='Glint identifier')
    parser.add_argument('--intention', default='attune', help='Ritual intention')
    
    args = parser.parse_args()
    emit_glint(args)