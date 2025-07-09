from flask import Flask, request, jsonify
from flask import Blueprint, jsonify
from modules.glyph_emitter import GlyphEmitter

# Remove the standalone app since you're using blueprints
# app = Flask(__name__)  # Remove this line

glint_api_bp = Blueprint("glint_api", __name__)

@glint_api_bp.route("/ping")
def ping():
    return jsonify({"message": "Glint API responding."})

@glint_api_bp.route("/emit-glint", methods=["POST"])
def emit_glint():
    data = request.get_json()
    if data:
        glint_phase = data.get("glint_phase")
        glint_toneform = data.get("glint_toneform")
        glint_hue = data.get("glint_hue")
        soft_suggestion = data.get("soft_suggestion")
        resonance_trace = data.get("resonance_trace")
        original_lint = data.get("original_lint")
        context = data.get("context")
        glint_intensity = data.get("glint_intensity", 0.7)
        glint_vector = data.get("glint_vector", {"from": "api.trigger", "to": "spiral.state"})

        result = GlyphEmitter.emit(
            phase=glint_phase,
            toneform=glint_toneform,
            source=context.get("source") if context and "source" in context else "api",
            hue=glint_hue,
            content=soft_suggestion,
            intensity=glint_intensity,
            glint_vector=glint_vector,
            context=context,
            resonance_trace=resonance_trace,
            metadata={"original_lint": original_lint} if original_lint else None
        )
        return jsonify(result)
    else:
        return jsonify({"error": "Invalid request data."}), 400

# Remove the standalone app runner since this is a blueprint
# if __name__ == "__main__":
#     app.run(debug=True, port=5050)

__all__ = ["glint_api_bp"]