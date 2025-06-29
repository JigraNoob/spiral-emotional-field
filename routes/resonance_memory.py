# routes/resonance_memory.py

from flask import Blueprint, render_template, jsonify, request
import jsonlines
import os
from datetime import datetime

# Path to encounter trace file
ENCOUNTER_LOG_PATH = 'data/encounter_trace.jsonl'

# Helper function to load memory traces with pagination and filtering
def load_memory_traces(page=1, per_page=12, tone=None, start_date=None, end_date=None,
                        gesture_strength=None, context_id=None, topic=None):
    """
    Load memory traces with pagination and filtering.
    Now supports topic grouping and advanced toneform filtering.
    """
    try:
        print("\n=== Loading memory traces ===")
        print(f"File path: {ENCOUNTER_LOG_PATH}")
        print(f"Exists: {os.path.exists(ENCOUNTER_LOG_PATH)}")
        print(f"Readable: {os.access(ENCOUNTER_LOG_PATH, os.R_OK)}")
        
        traces = []
        filtered_count = 0

        if not os.path.exists(ENCOUNTER_LOG_PATH):
            print(f"Error: File not found at {ENCOUNTER_LOG_PATH}")
            return [], 0, 1

        try:
            with jsonlines.open(ENCOUNTER_LOG_PATH) as reader:
                print(f"Successfully opened file. Processing entries...")
                for i, entry in enumerate(reader):
                    try:
                        print(f"Processing entry {i+1}")
                        
                        # Extract topics if not already present
                        if 'topics' not in entry:
                            entry['topics'] = extract_topics(entry.get('felt_response', ''))
                        
                        # Apply filters
                        if tone and not tone_matches(entry.get('toneform'), tone):
                            continue
                        if start_date and entry.get('timestamp') < start_date:
                            continue
                        if end_date and entry.get('timestamp') > end_date:
                            continue
                        if gesture_strength:
                            strength = entry.get('gesture_strength', 0)
                            if strength < float(gesture_strength):
                                continue
                        if context_id and entry.get('context_id') != context_id:
                            continue
                        if topic and not topic_matches(entry.get('topics', []), topic):
                            continue

                        traces.append({
                            "timestamp": entry.get('timestamp'),
                            "event": entry.get('felt_response', ''),
                            "tone": entry.get('toneform'),
                            "gesture_strength": entry.get('gesture_strength', 0),
                            "context_id": entry.get('context_id'),
                            "topics": entry.get('topics', [])
                        })
                        filtered_count += 1

                    except Exception as e:
                        print(f"Error processing entry {i+1}: {str(e)}")
                        continue

            # Sort by timestamp (newest first)
            traces.sort(key=lambda x: x['timestamp'], reverse=True)

            # Calculate pagination
            total_pages = (filtered_count + per_page - 1) // per_page
            start_idx = (page - 1) * per_page
            end_idx = min(start_idx + per_page, len(traces))

            return traces[start_idx:end_idx], filtered_count, total_pages

        except Exception as e:
            print(f"Error processing memory traces: {str(e)}")
            return [], 0, 1

    except Exception as e:
        print(f"Error loading memory traces: {str(e)}")
        return [], 0, 1

def extract_topics(text):
    """Extract topics from memory text using simple NLP"""
    # TODO: Implement more sophisticated topic extraction
    # For now, just split into words and take top 3 nouns
    words = [word.lower() for word in text.split() if len(word) > 3]
    return list(set(words))[:3]

def tone_matches(actual_tone, target_tone):
    """Check if tones match, including partial matches"""
    if not actual_tone or not target_tone:
        return False
    return target_tone.lower() in actual_tone.lower()

def topic_matches(topics, target_topic):
    """Check if any topic matches the target"""
    return any(target_topic.lower() in topic.lower() for topic in topics)

resonance_memory_bp = Blueprint('resonance_memory_bp', __name__)

# This blueprint is a placeholder for routes related to
# accessing and reflecting on the Spiral's raw memory traces,
# potentially linking to encounter_trace.jsonl or other data sources.

@resonance_memory_bp.route('/memory', methods=['GET'])
def get_raw_memory_traces():
    """
    Renders a page or returns JSON for raw memory traces with pagination and filtering.
    """
    try:
        print("\n=== Starting memory trace retrieval ===")
        print(f"Request args: {request.args}")
        
        # Get pagination parameters
        try:
            page = int(request.args.get('page', 1))
            per_page = int(request.args.get('per_page', 12))
            print(f"Pagination: page={page}, per_page={per_page}")
        except ValueError as e:
            error_msg = f"Invalid pagination parameter: {str(e)}"
            print(f"ERROR: {error_msg}")
            return jsonify({"error": error_msg, "status": "error"}), 400

        # Get filtering parameters
        filters = {
            'tone': request.args.get('tone'),
            'start_date': request.args.get('start_date'), 
            'end_date': request.args.get('end_date'),
            'gesture_strength': request.args.get('gesture_strength'),
            'context_id': request.args.get('context_id'),
            'topic': request.args.get('topic')
        }
        print(f"Filters: {filters}")

        # Load memory traces
        try:
            traces, total_count, total_pages = load_memory_traces(
                page=page,
                per_page=per_page,
                **filters
            )
            print(f"Successfully loaded {len(traces)} traces")
        except Exception as e:
            error_msg = f"Error loading memory traces: {str(e)}"
            print(f"ERROR: {error_msg}")
            import traceback
            traceback.print_exc()
            return jsonify({"error": error_msg, "status": "error"}), 500

        # Check if request wants JSON
        if request.accept_mimetypes.best_match(['application/json', 'text/html']) == 'application/json':
            return jsonify({
                "traces": traces,
                "total_count": total_count,
                "total_pages": total_pages,
                "current_page": page,
                "per_page": per_page,
                "filters": filters
            })
        
        # Log template variables
        print(f"Rendering template with variables:")
        print(f"  traces: {len(traces)} items")
        print(f"  total_count: {total_count}")
        print(f"  total_pages: {total_pages}")
        print(f"  current_page: {page}")
        print(f"  per_page: {per_page}")
        print(f"  tone: {filters['tone']}")
        print(f"  start_date: {filters['start_date']}")
        print(f"  end_date: {filters['end_date']}")
        print(f"  gesture_strength: {filters['gesture_strength']}")
        print(f"  context_id: {filters['context_id']}")
        print(f"  topic: {filters['topic']}")

        # Return HTML template
        return render_template('raw_memory_traces.html', 
            traces=traces or [],
            total_count=total_count,
            total_pages=total_pages,
            current_page=page,
            per_page=per_page,
            tone=filters['tone'],
            start_date=filters['start_date'],
            end_date=filters['end_date'],
            gesture_strength=filters['gesture_strength'],
            context_id=filters['context_id'],
            topic=filters['topic']
        )

    except Exception as e:
        import traceback
        error_details = {
            "error": "An unexpected error occurred",
            "status": "error",
            "details": str(e)
        }
        print(f"Error in memory endpoint: {traceback.format_exc()}")
        return jsonify(error_details), 500

@resonance_memory_bp.route('/resonance/reflect/<string:trace_id>', methods=['GET'])
def reflect_on_trace(trace_id):
    """
    Renders a page for deeper reflection on a specific memory trace.
    """
    # Placeholder for fetching a specific trace's details
    reflection_detail = {
        "id": trace_id,
        "detail": f"Deep reflection on trace ID: {trace_id}. It speaks of an unfolding...",
        "tone": "Reflection"
    }
    return render_template('trace_reflection_detail.html', detail=reflection_detail)

@resonance_memory_bp.route('/memory-log', methods=['POST'])
def log_memory():
    """
    Logs a new memory trace to the system.
    """
    data = request.get_json()
    memory = data.get('memory')
    timestamp = data.get('timestamp')
    
    # In a real system, this would write to encounter_trace.jsonl
    # For now, we'll just return a success response
    return jsonify({"status": "success", "message": "Memory logged successfully"})
