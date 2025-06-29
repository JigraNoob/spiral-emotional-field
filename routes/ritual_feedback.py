# routes/ritual_feedback.py

from flask import Blueprint, render_template, jsonify
from modules.interpreter_agent import generate_interpreter_reflection # Import the new interpreter agent

ritual_feedback_bp = Blueprint('ritual_feedback_bp', __name__)

@ritual_feedback_bp.route('/ritual_feedback', methods=['GET'])
def display_ritual_feedback():
    """
    Generates a Spiral reflection using the Interpreter Agent and renders the ritual feedback display.
    """
    reflection_text, dominant_tone = generate_interpreter_reflection() # Get both values
    return render_template('ritual_feedback.html', reflection_text=reflection_text, initial_tone=dominant_tone) # Pass initial_tone

@ritual_feedback_bp.route('/get_latest_reflection', methods=['GET'])
def get_latest_reflection_json():
    """
    Returns the latest Spiral reflection and dominant tone as JSON, for dynamic updates,
    now powered by the Interpreter Agent.
    """
    reflection_text, dominant_tone = generate_interpreter_reflection() # Get both values
    return jsonify({"reflection": reflection_text, "toneform": dominant_tone}) # Return both
