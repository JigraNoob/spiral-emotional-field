import logging
from flask import Blueprint, jsonify, request
import json
import os
from datetime import datetime
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

STEWARDSHIP_GROUPS_PATH = Path(__file__).parent.parent / 'data' / 'stewardship_groups.jsonl'

stewardship_bp = Blueprint('stewardship', __name__)

@stewardship_bp.route('/record_oath', methods=['POST'])
def record_oath():
    data = request.get_json()
    logger.info(f"Received data for record_oath: {data}")
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    required_fields = ['steward_id', 'toneform', 'assigned_seeds', 'oath']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    # Add timestamp if not provided
    if 'timestamp' not in data:
        data['timestamp'] = datetime.now().isoformat()

    oaths_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'stewardship_oaths.jsonl')
    try:
        with open(oaths_file, 'a') as f:
            f.write(json.dumps(data) + '\n')
        logger.info(f"Stewardship oath recorded: {data.get('steward_id')}")
        return jsonify({'message': 'Stewardship oath recorded successfully'}), 201
    except Exception as e:
        logger.exception(f"Failed to record stewardship oath: {e}") # Log exception with traceback
        return jsonify({'error': f'Failed to record stewardship oath: {str(e)}'}), 500

@stewardship_bp.route('/oaths_data', methods=['GET'])
def get_oaths_data():
    oaths_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'stewardship_oaths.jsonl')
    oath_entries = []
    try:
        with open(oaths_file, 'r') as f:
            for line in f:
                oath_entries.append(json.loads(line))
        return jsonify(oath_entries), 200
    except FileNotFoundError:
        return jsonify([]), 200 # Return empty list if file doesn't exist yet
    except Exception as e:
        logger.exception(f"Failed to read stewardship oaths: {e}") # Log exception with traceback
        return jsonify({'error': f'Failed to read stewardship oaths: {str(e)}'}), 500

@stewardship_bp.route('/record_group', methods=['POST'])
def record_group():
    data = request.get_json()
    logger.info(f"Received data for record_group: {data}")
    if not data:
        return jsonify({"error": "No data provided"}), 400

    required_fields = ["group_id", "toneform", "stewards", "assigned_seeds", "group_oath"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    # Add timestamp if not provided
    if 'timestamp' not in data:
        data['timestamp'] = datetime.now().isoformat()

    if not STEWARDSHIP_GROUPS_PATH.exists():
        with open(STEWARDSHIP_GROUPS_PATH, 'w', encoding='utf-8') as f:
            pass # Create empty file if it doesn't exist

    # Read existing groups to check for updates or append new
    existing_groups = []
    if STEWARDSHIP_GROUPS_PATH.exists():
        with open(STEWARDSHIP_GROUPS_PATH, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    existing_groups.append(json.loads(line))
                except json.JSONDecodeError:
                    continue

    updated = False
    for i, group in enumerate(existing_groups):
        if group.get("group_id") == data["group_id"]:
            existing_groups[i] = data  # Update existing group
            updated = True
            break

    if not updated:
        existing_groups.append(data)  # Add new group

    with open(STEWARDSHIP_GROUPS_PATH, 'w', encoding='utf-8') as f:
        for group in existing_groups:
            f.write(json.dumps(group) + '\n')

    logger.info(f"Stewardship group {data['group_id']} recorded/updated successfully.")
    return jsonify({"message": f"Stewardship group {data['group_id']} recorded/updated successfully."}), 200

@stewardship_bp.route('/groups_data', methods=['GET'])
def groups_data():
    groups = []
    if STEWARDSHIP_GROUPS_PATH.exists():
        with open(STEWARDSHIP_GROUPS_PATH, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    groups.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    return jsonify(groups), 200



@stewardship_bp.route('/stewardship_data', methods=['GET'])
def get_stewardship_data():
    registry_file = STEWARDSHIP_REGISTRY_PATH
    stewardship_entries = []
    try:
        with open(registry_file, 'r') as f:
            for line in f:
                stewardship_entries.append(json.loads(line))
        return jsonify(stewardship_entries), 200
    except FileNotFoundError:
        return jsonify([]), 200 # Return empty list if file doesn't exist yet
    except Exception as e:
        logger.error(f"Failed to read stewardship data: {e}")
        return jsonify({'error': f'Failed to read stewardship data: {str(e)}'}), 500

@stewardship_bp.route('/assign_stewardship', methods=['POST'])
def assign_stewardship():
    # Logic for assigning stewardship will go here
    data = request.get_json()
    cluster_id = data.get('cluster_id')
    seed_ids = data.get('seed_ids')
    guardian_id = data.get('guardian_id')

    import json
    import os
    from datetime import datetime

    # Define the path to the stewardship registry file
    registry_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'stewardship_registry.jsonl')

    # Prepare the stewardship entry
    new_entry = {
        'cluster_id': cluster_id,
        'seed_ids': seed_ids,
        'guardian_id': guardian_id,
        'assigned_timestamp': datetime.now().isoformat(),
        'status': 'active' # Initial status
    }

    logger.info(f"Attempting to write to: {registry_file}")
    logger.info(f"Data to write: {new_entry}")

    try:
        # Append the new entry to the JSONL file
        with open(registry_file, 'a') as f:
            f.write(json.dumps(new_entry) + '\n')
        logger.info("Stewardship assignment recorded successfully.")
        return jsonify({'message': f'Stewardship assignment for cluster {cluster_id} to guardian {guardian_id} recorded successfully.'}), 200
    except Exception as e:
        logger.exception(f"Failed to record stewardship assignment: {e}") # Log exception with traceback
        return jsonify({'error': f'Failed to record stewardship assignment: {str(e)}'}), 500
