from flask import Blueprint, send_file, jsonify, request
import os
import json
import io
import jsonlines
from datetime import datetime

# Blueprint for exporting individual memory echoes
echo_export_bp = Blueprint('echo_export', __name__)

MEMORY_PATH = "data/memory_shards.jsonl"

def log_export_action(echo_id, format_type, toneform=None):
    log_entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "echo_id": echo_id,
        "format": format_type,
        "toneform": toneform
    }
    log_path = "data/export_log.jsonl"
    try:
        with jsonlines.open(log_path, mode='a') as writer:
            writer.write(log_entry)
    except Exception as e:
        print(f"Export log failed: {e}")

@echo_export_bp.route("/export/echo/<echo_id>", methods=["GET"])
def export_echo(echo_id):
    export_format = request.args.get("format", "json")
    if not os.path.exists(MEMORY_PATH):
        return jsonify({"error": "Memory archive not found"}), 404

    with open(MEMORY_PATH, "r", encoding="utf-8") as f:
        for line in f:
            memory = json.loads(line)
            if memory.get("id") == echo_id:
                if export_format == "poem":
                    poetic_text = generate_poetic_echo(memory)
                    log_export_action(echo_id, export_format, memory.get('toneform'))
                    return send_file(
                        io.BytesIO(poetic_text.encode("utf-8")),
                        mimetype="text/plain",
                        as_attachment=True,
                        download_name=f"{echo_id}_poem.txt"
                    )
                else:
                    log_export_action(echo_id, export_format, memory.get('toneform'))
                    return jsonify(memory)
    return jsonify({"error": "Echo not found"}), 404

def generate_poetic_echo(memory):
    return f"""🌫️ Echo Memory — {memory.get("toneform", "Unknown")}

ID: {memory.get("id")}
Timestamp: {memory.get("timestamp")}

Gesture:
{memory.get("gesture", "[no trace]")}

Murmur:
{memory.get("murmur", "[silent]")}

Toneform Drift:
{memory.get("toneform_description", "[undrawn]")}
"""
