# routes/get_historical_murmurs.py

from flask import Blueprint, jsonify
import jsonlines
import os
import random

get_historical_murmurs_bp = Blueprint('get_historical_murmurs_bp', __name__)

ENCOUNTER_LOG_PATH = 'data/encounter_trace.jsonl'

def load_encounter_murmurs(page=1, per_page=12, toneform=None, start_date=None, end_date=None):
    """
    Load historical murmurs with pagination and filtering.
    Returns a tuple of (murmurs, total_count, total_pages).
    """
    try:
        murmurs = []
        filtered_count = 0

        print(f"Loading murmurs from {ENCOUNTER_LOG_PATH}")
        print(f"Filters: toneform={toneform}, start_date={start_date}, end_date={end_date}")

        if not os.path.exists(ENCOUNTER_LOG_PATH):
            print(f"Warning: Encounter log file not found at {ENCOUNTER_LOG_PATH}")
            return [], 0, 1

        try:
            with jsonlines.open(ENCOUNTER_LOG_PATH) as reader:
                for i, entry in enumerate(reader):
                    try:
                        if 'felt_response' in entry and 'toneform' in entry:
                            # Apply filters
                            if toneform and entry['toneform'] != toneform:
                                continue
                            if start_date and entry['timestamp'] < start_date:
                                continue
                            if end_date and entry['timestamp'] > end_date:
                                continue

                            murmurs.append({
                                "text": entry['felt_response'],
                                "toneform": entry['toneform'],
                                "timestamp": entry['timestamp']
                            })
                            filtered_count += 1
                    except Exception as e:
                        print(f"Error processing entry {i+1}: {str(e)}")
                        continue

            print(f"Total murmurs: {len(murmurs)}, filtered count: {filtered_count}")
            
            # Sort by timestamp (newest first)
            murmurs.sort(key=lambda x: x['timestamp'], reverse=True)

            # Calculate pagination
            total_pages = (filtered_count + per_page - 1) // per_page
            start_idx = (page - 1) * per_page
            end_idx = min(start_idx + per_page, len(murmurs))

            print(f"Returning page {page} with {end_idx - start_idx} murmurs out of {filtered_count} total")
            print(f"Total pages: {total_pages}")

            # Return paginated results, total count, and total pages
            return murmurs[start_idx:end_idx], filtered_count, total_pages

        except jsonlines.jsonlines.InvalidLineError as e:
            print(f"Error reading JSON Lines file: {str(e)}")
            return [], 0, 1
        except Exception as e:
            print(f"Error processing murmurs: {str(e)}")
            return [], 0, 1

    except Exception as e:
        print(f"Error loading murmurs: {str(e)}")
        return [], 0, 1

@get_historical_murmurs_bp.route('/get_historical_murmurs', methods=['GET'])
def get_historical_murmurs():
    try:
        # Validate pagination parameters
        try:
            page = int(request.args.get('page', 1))
            if page < 1:
                raise ValueError("Page must be greater than 0")
            
            per_page = int(request.args.get('per_page', 12))
            if per_page < 1:
                raise ValueError("Per page must be greater than 0")
        except ValueError as e:
            return jsonify({
                "error": f"Invalid pagination parameter: {str(e)}",
                "status": "error"
            }), 400
        
        # Get filtering parameters
        toneform = request.args.get('toneform')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')

        try:
            # Load murmurs with pagination and filtering
            murmurs, total_count, total_pages = load_encounter_murmurs(
                page=page,
                per_page=per_page,
                toneform=toneform,
                start_date=start_date,
                end_date=end_date
            )

            return jsonify({
                "murmurs": murmurs,
                "total_count": total_count,
                "total_pages": total_pages,
                "current_page": page,
                "per_page": per_page,
                "filters": {
                    "toneform": toneform,
                    "start_date": start_date,
                    "end_date": end_date
                }
            })

        except Exception as e:
            return jsonify({
                "error": f"Error loading murmurs: {str(e)}",
                "status": "error"
            }), 500

    except Exception as e:
        import traceback
        error_details = {
            "error": "An unexpected error occurred",
            "status": "error",
            "details": str(e)
        }
        print(f"Error in murmurs endpoint: {traceback.format_exc()}")
        return jsonify(error_details), 500
