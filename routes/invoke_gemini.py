# routes/invoke_gemini.py

from flask import Blueprint, request, jsonify
import json
import os
import google.generativeai as genai
import jsonlines # NEW: Import jsonlines for appending to JSONL file
from datetime import datetime # NEW: Import datetime for current timestamp

invoke_gemini_bp = Blueprint('invoke_gemini_bp', __name__)

# Define the path to encounter_trace.jsonl
ENCOUNTER_TRACE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'encounter_trace.jsonl')


@invoke_gemini_bp.route('/invoke_gemini', methods=['POST'])
def invoke_gemini():
    """
    Receives recent toneform data, crafts a prompt, invokes the Gemini API,
    returns a generated memory poem and suggested shimmer toneform,
    and archives the poem as a 'poem' echo in encounter_trace.jsonl.
    """
    try:
        data = request.get_json()
        if not data or 'recent_toneforms' not in data:
            return jsonify({"status": "error", "message": "No recent toneforms data provided."}), 400

        recent_toneforms = data['recent_toneforms']
        
        # --- Authoring a Prompt Structure for structured output ---
        all_toneforms = [
            "Coherence", "Presence", "Curiosity", "Trust", "Reflection",
            "Resonance", "Memory", "Stillness", "Longing", "Adaptation"
        ]
        toneform_list_str = ", ".join(all_toneforms)

        if not recent_toneforms:
            prompt_text = (
                "Compose a brief, ambient memory poem (3-5 lines) about stillness and quiet reflection. "
                "Also, suggest a single dominant toneform from the list: "
                f"[{toneform_list_str}] that best represents the poem's feeling for a visual shimmer."
            )
        else:
            toneform_gestures = ", ".join(recent_toneforms)
            prompt_text = (
                f"Based on recent toneform gestures experienced in a digital shrine, which include: {toneform_gestures}. "
                f"Compose a short, ethereal memory poem (3-5 lines) that the shrine might whisper, "
                f"reflecting on these combined tones. Focus on evocative imagery and a sense of gentle resonance. "
                f"Also, from the list [{toneform_list_str}], suggest the single most fitting toneform "
                f"to represent the poem's core feeling for a visual shimmer. Return your response as a JSON object."
            )

        print(f"Gemini Invocation Prompt: {prompt_text}")

        # --- Invoke Gemini API with structured response configuration ---
        model = genai.GenerativeModel('gemini-2.0-flash')
        
        generation_config = {
            "response_mime_type": "application/json",
            "response_schema": {
                "type": "OBJECT",
                "properties": {
                    "poem": {"type": "STRING", "description": "The generated memory poem."},
                    "shimmer_toneform": {"type": "STRING", "description": "The toneform suggested for visual shimmer."}
                },
                "required": ["poem", "shimmer_toneform"]
            }
        }
        
        response = model.generate_content(prompt_text, generation_config=generation_config)

        if response and response.candidates:
            json_str = response.candidates[0].content.parts[0].text
            generated_data = json.loads(json_str)
            
            generated_poem = generated_data.get('poem')
            shimmer_toneform = generated_data.get('shimmer_toneform')

            if generated_poem and shimmer_toneform:
                print(f"Gemini Generated Poem:\n{generated_poem}")
                print(f"Suggested Shimmer Toneform: {shimmer_toneform}")

                # NEW: Archive the Gemini poem as an echo in encounter_trace.jsonl
                poem_echo_entry = {
                    "timestamp": datetime.now().isoformat(),
                    "echo_type": "poem", # Designating this as a 'poem' echo type
                    "toneform": shimmer_toneform, # Using the shimmer_toneform as the primary toneform for the echo
                    "felt_response": generated_poem,
                    "context_id": "gemini_synthesis", # A unique ID for Gemini-generated content
                    "gesture_strength": 0.8, # Assign a default strength for its visual representation
                    "orb_color": None # Let the breathline map use its default color mapping for this toneform
                }
                # Ensure the data directory exists
                data_dir = os.path.dirname(ENCOUNTER_TRACE_FILE)
                os.makedirs(data_dir, exist_ok=True)
                
                with jsonlines.open(ENCOUNTER_TRACE_FILE, mode='a') as writer:
                    writer.write(poem_echo_entry)
                print(f"Archived Gemini poem to {ENCOUNTER_TRACE_FILE}")

                return jsonify({"status": "success", "poem": generated_poem, "shimmer_toneform": shimmer_toneform}), 200
            else:
                print("Gemini API did not return expected structured content (poem or shimmer_toneform missing). Details: " + json_str)
                return jsonify({"status": "error", "message": "Gemini API did not return expected structured content (poem or shimmer_toneform missing). Details: " + json_str}), 500
        else:
            print("Gemini API did not return valid content.")
            return jsonify({"status": "error", "message": "Gemini API did not return valid content."}), 500

    except json.JSONDecodeError as jde:
        print(f"JSON decoding error from Gemini response: {jde}. Raw response: {json_str if 'json_str' in locals() else 'N/A'}")
        return jsonify({"status": "error", "message": f"Failed to parse Gemini JSON response: {jde}"}), 500
    except Exception as e:
        print(f"Error invoking Gemini: {e}")
        return jsonify({"status": "error", "message": f"An error occurred during Gemini invocation: {e}"}), 500

