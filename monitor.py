import requests
import time
from datetime import datetime
import json

with open('monitoring_config.json') as f:
    config = json.load(f)

def run_checks():
    for check in config['checks']:
        try:
            start = time.time()
            response = requests.get(check['url'], timeout=float(check['timeout'][:-1]))
            duration = time.time() - start
            
            if response.status_code == check['expect_status']:
                print(f"[{datetime.now()}] {check['name']} OK ({duration:.2f}s)")
            else:
                print(f"[{datetime.now()}] {check['name']} FAILED: Status {response.status_code}")
                # TODO: Trigger alert
        except Exception as e:
            print(f"[{datetime.now()}] {check['name']} ERROR: {str(e)}")
            # TODO: Trigger alert

if __name__ == "__main__":
    while True:
        run_checks()
        time.sleep(300)  # Run every 5 minutes
