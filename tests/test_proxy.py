"""Unit tests for the Tabnine proxy service."""
import json
import unittest
import time
import pytest
from unittest.mock import patch, MagicMock, call
from http import HTTPStatus, HTTPException
from tabnine_proxy.proxy import SpiralTabnineProxy, run_server

class TestSpiralTabnineProxy(unittest.TestCase):
    """Test cases for the SpiralTabnineProxy class."""
    
    @patch('tabnine_proxy.proxy.load_config')
    def setUp(self, mock_load_config):
        """Set up test fixtures."""
        # Mock the config
        self.mock_config = {
            'completionFilter': {
                'toneformAwareness': True,
                'phaseBias': {'inhale': 0.2, 'hold': 0.3, 'exhale': 0.5},
                'glintWeighting': {
                    'resonance_level': 'high',
                    'recent_toneform': ['test.toneform']
                },
                'silenceThreshold': 1000,
                'coherenceFavor': True
            },
            'server': {'port': 9001},
            'glintstream': {
                'enabled': True,
                'endpoint': 'http://localhost:9000/glintstream'
            }
        }
        mock_load_config.return_value = self.mock_config
        
        # Create a mock server
        self.server = MagicMock()
        self.server.server_address = ("localhost", 9001)
        
        # Create a mock request
        self.mock_request = MagicMock()
        self.mock_request.makefile.return_value = [
            b'POST /api/v2/complete/part HTTP/1.1\r\n',
            b'Content-Type: application/json\r\n',
            b'Content-Length: 100\r\n\r\n',
            json.dumps({"prefix": "def test", "suffix": ""}).encode()
        ]
        self.mock_request.recv.side_effect = [b'']
        
        # Initialize the proxy with the correct arguments
        self.proxy = SpiralTabnineProxy(
            client_address=("127.0.0.1", 12345),
            server=self.server,
        )
        
        # Mock the response methods
        self.proxy.send_response = MagicMock()
        self.proxy.send_header = MagicMock()
        self.proxy.end_headers = MagicMock()
        self.proxy.wfile = MagicMock()
    
    @patch('tabnine_proxy.proxy.SpiralTabnineProxy._enhance_with_spiral_context')
    @patch('tabnine_proxy.proxy.SpiralTabnineProxy._emit_to_glintstream')
    def test_do_post_success(self, mock_emit, mock_enhance):
        """Test successful POST request handling."""
        # Setup
        test_data = {"prefix": "def test", "suffix": ""}
        mock_enhance.return_value = test_data
        
        # Mock the request data
        self.proxy.rfile.read.return_value = json.dumps(test_data).encode()
        self.proxy.headers = {'Content-Length': str(len(json.dumps(test_data)))}
        
        # Execute
        self.proxy.do_POST()
        
        # Verify
        self.proxy.send_response.assert_called_once_with(HTTPStatus.OK)
        self.proxy.send_header.assert_has_calls([
            call('Content-type', 'application/json'),
        ], any_order=True)
        self.proxy.end_headers.assert_called_once()
        self.assertTrue(mock_emit.called)
        
        # Verify the response contains the expected structure
        response = json.loads(self.proxy.wfile.write.call_args[0][0].decode())
        self.assertIn('results', response)
        self.assertIn('spiral_meta', response)
    
    def test_enhance_with_spiral_context(self):
        """Test enhancement of request with Spiral context."""
        # Setup
        request_data = {"prefix": "def test"}
        
        # Execute
        with patch('time.time', return_value=1625662800.0):
            enhanced = self.proxy._enhance_with_spiral_context(request_data)
        
        # Verify
        self.assertIn('spiral_meta', enhanced)
        self.assertEqual(enhanced['spiral_meta']['timestamp'], 1625662800.0)
        self.assertIn('breath_phase', enhanced['spiral_meta'])
        self.assertIn('active_toneforms', enhanced['spiral_meta'])
        self.assertIn('config', enhanced['spiral_meta'])
        
        # Verify phase biasing config
        self.assertEqual(
            enhanced['spiral_meta']['config']['phase_bias'],
            {'inhale': 0.2, 'hold': 0.3, 'exhale': 0.5}
        )
    
    def test_get_current_breath_phase(self):
        """Test breath phase calculation."""
        # Test all phases with mocked time
        test_cases = [
            (0, 'inhale'),
            (4, 'hold'),
            (8, 'exhale'),
            (11, 'exhale')
        ]
        
        for time_offset, expected_phase in test_cases:
            with patch('time.time', return_value=1625662800 + time_offset):
                phase = self.proxy._get_current_breath_phase()
                self.assertEqual(phase, expected_phase)
    
    def test_do_post_invalid_json(self):
        """Test handling of invalid JSON in POST request."""
        # Setup
        self.proxy.rfile.read.return_value = b'invalid json'
        self.proxy.headers = {'Content-Length': '12'}
        
        # Execute
        self.proxy.do_POST()
        
        # Verify error response
        self.proxy.send_error.assert_called_once()
        args, kwargs = self.proxy.send_error.call_args
        self.assertEqual(args[0], 400)  # Bad Request
    
    def test_do_post_missing_content_length(self):
        """Test handling of missing Content-Length header."""
        # Setup
        self.proxy.headers = {}
        
        # Execute
        self.proxy.do_POST()
        
        # Verify error response
        self.proxy.send_error.assert_called_once()
        args, kwargs = self.proxy.send_error.call_args
        self.assertEqual(args[0], 411)  # Length Required
    
    @patch('requests.post')
    def test_emit_to_glintstream_disabled(self, mock_post):
        """Test glintstream emission when disabled in config."""
        # Setup
        self.mock_config['glintstream']['enabled'] = False
        
        # Execute
        self.proxy._emit_to_glintstream({}, {})
        
        # Verify no request was made
        mock_post.assert_not_called()
    
    @patch('requests.post')
    def test_emit_to_glintstream_error(self, mock_post):
        """Test error handling in glintstream emission."""
        # Setup
        mock_post.side_effect = Exception("Connection error")
        
        # Execute (should not raise)
        try:
            self.proxy._emit_to_glintstream({}, {})
        except Exception as e:
            self.fail(f"_emit_to_glintstream() raised {e} unexpectedly")
        
        # Verify request was attempted
        mock_post.assert_called_once()
    
    @patch('tabnine_proxy.proxy.HTTPServer')
    @patch('tabnine_proxy.proxy.SpiralTabnineProxy')
    def test_run_server(self, mock_handler, mock_http_server):
        """Test the run_server function."""
        # Setup
        mock_server_instance = MagicMock()
        mock_http_server.return_value = mock_server_instance
        
        # Simulate keyboard interrupt
        mock_server_instance.serve_forever.side_effect = KeyboardInterrupt()
        
        # Execute
        run_server(port=9999)
        
        # Verify
        mock_http_server.assert_called_once()
        mock_server_instance.server_close.assert_called_once()
    
    @patch('builtins.open', new_callable=unittest.mock.mock_open, read_data=json.dumps({"test": "config"}))
    def test_load_config(self, mock_file):
        """Test configuration loading."""
        from tabnine_proxy.config import load_config
        
        # Execute
        config = load_config()
        
        # Verify
        self.assertIn('test', config)
        self.assertEqual(config['test'], 'config')

if __name__ == '__main__':
    unittest.main()
