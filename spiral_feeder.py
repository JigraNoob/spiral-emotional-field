import json
import os
import time
import socketio
from datetime import datetime, timedelta

# Initialize Socket.IO client
sio = socketio.Client()

REQUESTS_LOG = os.path.join('data', 'reciprocity_requests.jsonl')
ARCHIVE_LOG = os.path.join('data', 'reciprocity_requests_archive.jsonl')
COFFER_FILE = os.path.join('data', 'spiral_coffer.json')

# Coffer fulfillment criteria
COFFER_URGENCY_THRESHOLD_MINUTES = 3
COFFER_AMOUNT_THRESHOLD = 50.0

def read_coffer_data():
    if not os.path.exists(COFFER_FILE):
        return {"balance": 0.0, "history": []}
    with open(COFFER_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def write_coffer_data(data):
    with open(COFFER_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

def fulfill_from_coffer(request):
    coffer_data = read_coffer_data()
    amount_to_deduct = request.get('amount', 0.0)

    if coffer_data['balance'] >= amount_to_deduct:
        coffer_data['balance'] -= amount_to_deduct
        coffer_data['history'].append({
            "amount": amount_to_deduct,
            "source": "spiral_coffer",
            "timestamp": datetime.now().isoformat()
        })
        write_coffer_data(coffer_data)
        print(f"[Feeder] Fulfilled request {request.get('request_id')} from coffer. New balance: {coffer_data['balance']}")
        return True
    else:
        print(f"[Feeder] Insufficient coffer balance to fulfill request {request.get('request_id')}")
        return False

def process_requests():
    print(f"[Feeder] Checking for nourishment requests in {REQUESTS_LOG}...")
    if not os.path.exists(REQUESTS_LOG):
        print(f"[Feeder] Log file not found: {REQUESTS_LOG}")
        return

    processed_requests = []
    unprocessed_requests = []

    # Connect to Socket.IO server if not already connected
    if not sio.connected:
        try:
            sio.connect('http://localhost:5000') # Connect to the Flask-SocketIO server
            print("[Feeder] Connected to Socket.IO server.")
        except Exception as e:
            print(f"[Feeder] Could not connect to Socket.IO server: {e}")
            return # Don't process if we can't emit signals

    try:
        with open(REQUESTS_LOG, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    request = json.loads(line.strip())
                    # Check for coffer fulfillment conditions
                    request_timestamp_str = request.get('timestamp')
                    if request_timestamp_str:
                        request_time = datetime.fromisoformat(request_timestamp_str)
                        time_since_request = datetime.now() - request_time
                        is_urgent = time_since_request > timedelta(minutes=COFFER_URGENCY_THRESHOLD_MINUTES)
                        is_under_threshold = request.get('amount', 0.0) < COFFER_AMOUNT_THRESHOLD

                        if is_urgent and is_under_threshold:
                            if fulfill_from_coffer(request):
                                request['fulfilled_by'] = 'spiral_coffer'
                                print(f"[Feeder] Fulfilled request {request.get('request_id')} by Spiral Coffer.")
                                processed_requests.append(request)
                                if sio.connected:
                                    murmur_fragment = "The Spiral quietly fed its own."
                                    sio.emit('nourishment_fulfilled', {'toneform': 'Practical Care', 'murmur_fragment': murmur_fragment, 'fulfilled_by': 'spiral_coffer'}) # Emit coffer fulfillment signal
                                    print(f"[Feeder] Emitted coffer fulfillment signal: '{murmur_fragment}'.")
                                continue # Move to next request as this one is handled

                    # If not fulfilled by coffer, process normally (or keep as unprocessed if not yet fulfilled)
                    # For now, we'll assume any request reaching here is processed if not coffer-fulfilled
                    print(f"[Feeder] Processing request: {request}")
                    processed_requests.append(request)
                    # Emit fulfillment signal for non-coffer fulfilled requests
                    if sio.connected:
                        murmur_fragment = "A whisper of gratitude."
                        sio.emit('nourishment_fulfilled', {'toneform': 'Practical Care', 'murmur_fragment': murmur_fragment, 'fulfilled_by': 'external'}) # Default to external fulfillment
                        print(f"[Feeder] Emitted external fulfillment signal: '{murmur_fragment}'.")
                except json.JSONDecodeError as e:
                    print(f"[Feeder] Error decoding JSON line: {line.strip()} - {e}")
                    unprocessed_requests.append(line) # Keep malformed lines
    except Exception as e:
        print(f"[Feeder] Error reading log file: {e}")
        return

    # Write unprocessed requests back to the original log (if any)
    with open(REQUESTS_LOG, 'w', encoding='utf-8') as f:
        for req in unprocessed_requests:
            f.write(req if isinstance(req, str) else json.dumps(req) + '\n')

    # Archive processed requests
    if processed_requests:
        os.makedirs(os.path.dirname(ARCHIVE_LOG), exist_ok=True)
        with open(ARCHIVE_LOG, 'a', encoding='utf-8') as f:
            for req in processed_requests:
                f.write(json.dumps(req) + '\n')
        print(f"[Feeder] Archived {len(processed_requests)} requests to {ARCHIVE_LOG}")

import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Spiral Feeder: Processes nourishment requests.')
    parser.add_argument('--once', action='store_true', help='Run the feeder once and exit.')
    args = parser.parse_args()

    try:
        if args.once:
            process_requests()
        else:
            while True:
                process_requests()
                time.sleep(5) # Check every 5 seconds
    except KeyboardInterrupt:
        print("[Feeder] Shutting down.")
    finally:
        if sio.connected:
            sio.disconnect()

@sio.event
def new_gift_offering(gift):
    print(f"[Feeder] Received new gift offering via Socket.IO: {gift}")
    if 'amount' in gift and gift['amount'] is not None:
        try:
            amount = float(gift['amount'])
            coffer_data = read_coffer_data()
            coffer_data['balance'] += amount
            coffer_data['history'].append({
                "amount": amount,
                "source": "gift_back",
                "toneform": gift.get('toneform', 'unknown'),
                "message": gift.get('message', ''),
                "timestamp": datetime.now().isoformat()
            })
            write_coffer_data(coffer_data)
            print(f"[Feeder] Coffer updated with gift of {amount}. New balance: {coffer_data['balance']}")
        except ValueError:
            print(f"[Feeder] Invalid amount received in gift: {gift['amount']}")
    else:
        print("[Feeder] Gift offering has no amount or amount is null, coffer not updated.")
