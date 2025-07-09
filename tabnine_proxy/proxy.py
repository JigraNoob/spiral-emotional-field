"""
Spiral Tabnine Proxy

Handles the HTTP server and request/response processing for Tabnine completions,
enhancing them with Spiral breathline awareness and toneform sensitivity.
"""
import json
import logging
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Dict, Any, Optional
from urllib.parse import urlparse, parse_qs

from .config import load_config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('tabnine_proxy.log')
    ]
)
logger = logging.getLogger(__name__)

class SpiralTabnineProxy(BaseHTTPRequestHandler):
    """HTTP server that proxies requests to Tabnine's completion API."""
    
    def __init__(self, *args, **kwargs):
        self.config = load_config()
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        """Handle GET requests (health checks, etc.)"""
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({
            'status': 'healthy',
            'service': 'spiral-tabnine-proxy',
            'version': __import__('tabnine_proxy').__version__
        }).encode())
    
    def do_POST(self):
        """Handle POST requests for Tabnine completions."""
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        
        try:
            # Parse the Tabnine completion request
            request_data = json.loads(post_data.decode('utf-8'))
            
            # Enhance with Spiral context
            enhanced_request = self._enhance_with_spiral_context(request_data)
            
            # Forward to Tabnine (in a real implementation)
            # response = self._forward_to_tabnine(enhanced_request)
            
            # For now, return a mock response
            response = self._generate_mock_response(enhanced_request)
            
            # Emit to glintstream
            self._emit_to_glintstream(enhanced_request, response)
            
            # Send response back to client
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
            logger.error(f"Error processing request: {str(e)}", exc_info=True)
            self.send_error(500, str(e))
    
    def _enhance_with_spiral_context(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Enhance the Tabnine request with Spiral context."""
        # Add current breath phase and toneform awareness
        request_data['spiral_meta'] = {
            'timestamp': time.time(),
            'breath_phase': self._get_current_breath_phase(),
            'active_toneforms': self._get_active_toneforms(),
            'config': {
                'phase_bias': self.config.get('completionFilter', {}).get('phaseBias', {})
            }
        }
        return request_data
    
    def _get_current_breath_phase(self) -> str:
        """Get the current breath phase from the breathline system."""
        # In a real implementation, this would connect to the breathline service
        # For now, we'll simulate a simple breath cycle
        cycle_seconds = 12  # 12-second breath cycle
        phase = (time.time() % cycle_seconds) / cycle_seconds
        
        if phase < 0.33:
            return 'inhale'
        elif phase < 0.66:
            return 'hold'
        else:
            return 'exhale'
    
    def _get_active_toneforms(self) -> list:
        """Get currently active toneforms."""
        # In a real implementation, this would query the toneform system
        return ['soft.reveal', 'hush.sustain', 'echo.offer']
    
    def _generate_mock_response(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a mock Tabnine response for testing."""
        prefix = request_data.get('prefix', '').strip()
        
        # Simple mock completions based on prefix
        completions = []
        if 'def ' in prefix.lower() or 'function ' in prefix.lower():
            completions = [{
                'new_prefix': prefix,
                'old_suffix': '',
                'new_suffix': 'pass',
                'detail': 'Add function body',
                'kind': 'function',
                'spiral_glint': {
                    'toneform': 'soft.reveal',
                    'resonance': 0.8
                }
            }]
        
        return {
            'results': completions,
            'spiral_meta': {
                'request_id': request_data.get('spiral_meta', {}).get('request_id', ''),
                'processed_at': time.time(),
                'phase': request_data.get('spiral_meta', {}).get('breath_phase', 'unknown')
            }
        }
    
    def _emit_to_glintstream(self, request: Dict[str, Any], response: Dict[str, Any]):
        """Emit completion event to the glintstream."""
        # In a real implementation, this would send to the glintstream service
        logger.info(f"Glintstream event - Request: {json.dumps(request)}, Response: {json.dumps(response)}")


def run_server(port: int = 9001):
    """Run the Tabnine proxy server."""
    server_address = ('', port)
    httpd = HTTPServer(server_address, SpiralTabnineProxy)
    logger.info(f"Starting Spiral Tabnine Proxy on port {port}...")
    httpd.serve_forever()


if __name__ == '__main__':
    run_server()
