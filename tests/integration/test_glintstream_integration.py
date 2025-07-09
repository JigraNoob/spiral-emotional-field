"""Integration tests for Glintstream interaction."""
import json
import unittest
import time
from unittest.mock import patch, MagicMock, call
import pytest
import requests
from tabnine_proxy.proxy import SpiralTabnineProxy

@pytest.mark.integration
class TestGlintstreamIntegration(unittest.TestCase):
    """Test integration with the Glintstream service."""
    
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
    
    @patch('requests.post')
    def test_emit_to_glintstream(self, mock_post):
        """Test emission of completion events to Glintstream."""
        # Setup
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response
        
        request = {
            "prefix": "def test",
            "spiral_meta": {
                "timestamp": 1625662800.0,
                "breath_phase": "exhale",
                "active_toneforms": ["test.toneform"]
            }
        }
        response = {
            "completion": "test completion",
            "spiral_meta": {
                "request_id": "test-request-123",
                "processed_at": 1625662801.0,
                "phase": "exhale"
            }
        }
        
        # Execute
        with patch('time.time', return_value=1625662802.0):
            self.proxy._emit_to_glintstream(request, response)
        
        # Verify the request
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        
        # Check URL and headers
        self.assertEqual(kwargs['url'], 'http://localhost:9000/glintstream')
        self.assertEqual(kwargs['headers'], {'Content-Type': 'application/json'})
        
        # Check payload structure
        payload = json.loads(kwargs['json'])
        self.assertEqual(payload['event_type'], 'completion')
        self.assertEqual(payload['timestamp'], 1625662802.0)
        
        # Check request/response data
        self.assertEqual(payload['request']['prefix'], 'def test')
        self.assertEqual(payload['response']['completion'], 'test completion')
        
        # Check Spiral metadata
        self.assertEqual(payload['metadata']['breath_phase'], 'exhale')
        self.assertEqual(payload['metadata']['toneforms'], ['test.toneform'])
    
    @patch('requests.post')
    def test_emit_to_glintstream_error_handling(self, mock_post):
        """Test error handling when Glintstream is unavailable."""
        # Setup
        mock_post.side_effect = requests.exceptions.ConnectionError("Connection error")
        
        request = {"prefix": "def test"}
        response = {"completion": "test completion"}
        
        # Mock logger to capture the error message
        with patch('tabnine_proxy.proxy.logger') as mock_logger:
            # Execute (should not raise)
            try:
                self.proxy._emit_to_glintstream(request, response)
            except Exception as e:
                self.fail(f"_emit_to_glintstream() raised {e} unexpectedly")
            
            # Verify error was logged
            mock_logger.error.assert_called_once()
            error_msg = mock_logger.error.call_args[0][0]
            self.assertIn("Failed to send to glintstream", error_msg)
    
    @patch('requests.post')
    def test_emit_to_glintstream_timeout(self, mock_post):
        """Test timeout handling when Glintstream is slow to respond."""
        # Setup
        mock_post.side_effect = requests.exceptions.Timeout("Request timed out")
        
        request = {"prefix": "def test"}
        response = {"completion": "test completion"}
        
        # Execute (should not raise)
        try:
            self.proxy._emit_to_glintstream(request, response)
        except Exception as e:
            self.fail(f"_emit_to_glintstream() raised {e} unexpectedly")
        
        # Verify request was made with timeout
        args, kwargs = mock_post.call_args
        self.assertEqual(kwargs['timeout'], 5.0)  # Default timeout
    
    @patch('requests.post')
    def test_emit_to_glintstream_http_error(self, mock_post):
        """Test handling of HTTP errors from Glintstream."""
        # Setup
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"
        mock_post.return_value = mock_response
        
        request = {"prefix": "def test"}
        response = {"completion": "test completion"}
        
        # Execute (should not raise)
        try:
            self.proxy._emit_to_glintstream(request, response)
        except Exception as e:
            self.fail(f"_emit_to_glintstream() raised {e} unexpectedly")
        
        # Verify request was made
        mock_post.assert_called_once()
    
    def test_glintstream_config_override(self):
        """Test that glintstream config can be overridden."""
        # Setup - override the config
        self.mock_config['glintstream'] = {
            'enabled': True,
            'endpoint': 'http://custom-glintstream:8080/api/events',
            'timeout': 2.5,
            'retries': 3
        }
        
        # Verify the config was updated
        self.assertEqual(
            self.proxy.config['glintstream']['endpoint'],
            'http://custom-glintstream:8080/api/events'
        )
        self.assertEqual(self.proxy.config['glintstream']['timeout'], 2.5)
        self.assertEqual(self.proxy.config['glintstream']['retries'], 3)
