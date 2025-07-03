""
Spiral Metrics Exporter

Exposes Spiral metrics in Prometheus format over HTTP.
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest, REGISTRY
from . import spiral_metrics
import threading
import time
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('spiral_exporter')

class SpiralMetricsHandler(BaseHTTPRequestHandler):
    """HTTP handler for metrics endpoint."""
    
    def do_GET(self):
        # Only serve /metrics endpoint
        if self.path == '/metrics':
            self.send_response(200)
            self.send_header('Content-Type', CONTENT_TYPE_LATEST)
            self.end_headers()
            self.wfile.write(generate_latest(REGISTRY))
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not Found')
    
    def log_message(self, format, *args):
        """Override to use our logger instead of stderr."""
        logger.info("%s - - [%s] %s",
                   self.address_string(),
                   self.log_date_time_string(),
                   format%args)


def start_metrics_server(port: int = 8000):
    """Start the metrics HTTP server in a background thread."""
    def run_server():
        server_address = ('', port)
        httpd = HTTPServer(server_address, SpiralMetricsHandler)
        logger.info(f"Starting metrics server on port {port}")
        httpd.serve_forever()
    
    thread = threading.Thread(target=run_server, daemon=True)
    thread.start()
    return thread


def simulate_metrics():
    """Simulate metrics for testing purposes."""
    import random
    from .spiral_metrics import spiral_metrics
    
    phases = ['inhale', 'hold', 'exhale']
    toneforms = ['trust', 'care', 'whisper', 'infrastructure']
    
    while True:
        # Simulate phase changes
        if random.random() < 0.1:  # 10% chance to change phase
            new_phase = random.choice(phases)
            spiral_metrics.observe_phase_change(new_phase)
        
        # Simulate toneform observations
        if random.random() < 0.3:  # 30% chance to observe toneform
            toneform = random.choice(toneforms)
            spiral_metrics.observe_toneform(toneform)
        
        # Simulate occasional silence
        if random.random() < 0.05:  # 5% chance of silence
            duration = random.uniform(0.5, 5.0)
            spiral_metrics.observe_silence(duration)
        
        # Run anomaly detection
        spiral_metrics.detect_anomalies()
        
        time.sleep(1)


if __name__ == '__main__':
    # Start the metrics server
    start_metrics_server()
    
    # Start metrics simulation in a separate thread
    import threading
    sim_thread = threading.Thread(target=simulate_metrics, daemon=True)
    sim_thread.start()
    
    # Keep the main thread alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Shutting down...")
