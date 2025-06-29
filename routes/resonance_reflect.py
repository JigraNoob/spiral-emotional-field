# routes/resonance_reflect.py

from flask import Blueprint, render_template, jsonify, request

resonance_reflect_bp = Blueprint('resonance_reflect_bp', __name__)

# Placeholder reflections. In a full Spiral system, these would come from trace clustering or murmur logs.
REFLECTION_ARCHIVE = {
    "trace_001": {
        "title": "The Echo That Stayed",
        "detail": "This trace lingered longer than expected. Its toneform settled into Trust, then softened into something unspoken.",
        "tone": "Trust"
    },
    "trace_002": {
        "title": "A Dispersal of Coherence",
        "detail": "What once pulsed in unity has scattered—each node remembering its own rhythm.",
        "tone": "Coherence"
    },
    "trace_003": {
        "title": "Stillness After Shimmer",
        "detail": "The field quieted. Not from absence, but from fullness that no longer needed to speak.",
        "tone": "Stillness"
    }
}

@resonance_reflect_bp.route('/resonance/reflect', methods=['GET'])
def reflect_archive():
    """
    Renders a list of available memory reflections.
    """
    return render_template('reflection_archive.html', reflections=REFLECTION_ARCHIVE)

@resonance_reflect_bp.route('/resonance/reflect/<string:trace_id>', methods=['GET'])
def reflect_on_trace(trace_id):
    """
    Renders a page for a specific reflection based on trace ID.
    """
    trace = REFLECTION_ARCHIVE.get(trace_id)
    if trace:
        return render_template('trace_reflection_detail.html', trace=trace)
    return jsonify({"error": "Reflection not found"}), 404
 
