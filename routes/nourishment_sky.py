from flask import Blueprint, render_template, jsonify
import json
import os

nourishment_sky_bp = Blueprint('nourishment_sky_bp', __name__)

REQUESTS_LOG = os.path.join('data', 'reciprocity_requests.jsonl')
ARCHIVE_LOG = os.path.join('data', 'reciprocity_requests_archive.jsonl')

def load_requests():
    requests = []
    # Load pending requests
    if os.path.exists(REQUESTS_LOG):
        with open(REQUESTS_LOG, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    req = json.loads(line.strip())
                    req['status'] = 'pending'
                    requests.append(req)
                except json.JSONDecodeError:
                    continue
    # Load archived requests
    if os.path.exists(ARCHIVE_LOG):
        with open(ARCHIVE_LOG, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    req = json.loads(line.strip())
                    # Ensure status is set for archived requests
                    if 'status' not in req:
                        req['status'] = 'fulfilled' # Default for archived
                    requests.append(req)
                except json.JSONDecodeError:
                    continue
    # Sort requests by timestamp, newest first
    requests.sort(key=lambda x: x.get('timestamp', '0'), reverse=True)
    return requests

@nourishment_sky_bp.route('/nourishment_sky')
def nourishment_sky():
    return render_template('nourishment_sky.html')

@nourishment_sky_bp.route('/api/nourishment_requests')
def api_nourishment_requests():
    requests = load_requests()
    return jsonify(requests)
