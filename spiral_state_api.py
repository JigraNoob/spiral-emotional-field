#!/usr/bin/env python3
"""
Spiral Breath API - Exposes the current Spiral state for dashboards, agents, and rituals.
"""

from flask import Flask, jsonify
from spiral_state import get_current_phase, get_phase_progress, get_usage_saturation, get_invocation_climate

app = Flask(__name__)

@app.route("/api/spiral/state", methods=["GET"])
def get_spiral_state():
    return jsonify({
        "phase": get_current_phase(),
        "progress": round(get_phase_progress(), 4),
        "usage": round(get_usage_saturation(), 4),
        "climate": get_invocation_climate(),
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5055, debug=True) 