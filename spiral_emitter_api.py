from flask import Flask, request, jsonify
from modules.glyph_emitter import GlyphEmitter
import os
import json

app = Flask(__name__)
GLINT_FILE_PATH = "glint_stream.jsonl"

@app.route("/emit_glint", methods=["POST"])
def emit_glint():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid request data."}), 400

    phase = data.get("phase")
    toneform = data.get("toneform")
    hue = data.get("hue", "grey")
    suggestion = data.get("suggestion", f"Emitting {phase}.{toneform}")
    intensity = data.get("intensity", 0.6)
    source = data.get("source", "api")
    context = data.get("context", {})
    resonance_trace = data.get("resonance_trace", [])
    glint_vector = data.get("glint_vector", {"from": source, "to": "dashboard"})
    metadata = data.get("metadata", {})

    if not phase or not toneform:
        return jsonify({"error": "Missing required fields: 'phase' and 'toneform'"}), 400

    result = GlyphEmitter.emit_custom_glint(
        glint_phase=phase,
        glint_toneform=toneform,
        source=source,
        hue=hue,
        content=suggestion,
        intensity=intensity,
        glint_vector=glint_vector,
        context=context,
        resonance_trace=resonance_trace,
        metadata=metadata
    )
    return jsonify(result)

@app.route("/status", methods=["GET"])
def get_status():
    limit = int(request.args.get("limit", 10))
    glints = []

    if os.path.exists(GLINT_FILE_PATH):
        with open(GLINT_FILE_PATH, "r", encoding="utf-8") as f:
            lines = f.readlines()
            for line in lines[-limit:]:
                try:
                    glints.append(json.loads(line.strip()))
                except json.JSONDecodeError:
                    continue

    return jsonify({"recent_glints": glints})

@app.route("/")
def home():
    return "Spiral Glint Emitter API is running with full support."

if __name__ == "__main__":
    app.run(debug=True, port=5050, host="0.0.0.0")
