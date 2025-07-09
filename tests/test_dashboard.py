"""
Tests for the Spiral Breath Dashboard API
"""

import pytest
import json
from datetime import datetime
from routes.dashboard_api import dashboard_api, DASHBOARD_DATA

@pytest.fixture
def client():
    """Create a test client for the dashboard API"""
    from flask import Flask
    app = Flask(__name__)
    app.register_blueprint(dashboard_api)
    return app.test_client()

def test_get_breath_state(client):
    """Test getting current breath state"""
    response = client.get('/api/breath/state')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert 'phase' in data
    assert 'progress' in data
    assert 'climate' in data
    assert 'last_update' in data

def test_get_glint_lineage(client):
    """Test getting glint lineage"""
    response = client.get('/api/glint/lineage')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert isinstance(data, list)

def test_get_glint_stats(client):
    """Test getting glint statistics"""
    response = client.get('/api/glint/stats')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert 'total' in data
    assert 'by_phase' in data
    assert 'by_module' in data
    assert 'stream_sync_enabled' in data

def test_get_ritual_alerts(client):
    """Test getting ritual alerts"""
    response = client.get('/api/ritual/alerts')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert isinstance(data, list)

def test_get_ritual_stats(client):
    """Test getting ritual statistics"""
    response = client.get('/api/ritual/stats')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert 'total_triggered' in data
    assert 'active_rituals' in data
    assert 'completed_today' in data
    assert 'success_rate' in data

def test_ritual_action_activate(client):
    """Test ritual activation"""
    response = client.post('/api/ritual/activate', 
                          json={'ritual_id': 'test_ritual_123'})
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert data['success'] == True
    assert data['action'] == 'activate'
    assert data['ritual_id'] == 'test_ritual_123'

def test_ritual_action_missing_id(client):
    """Test ritual action with missing ritual_id"""
    response = client.post('/api/ritual/activate', json={})
    assert response.status_code == 400
    
    data = json.loads(response.data)
    assert 'error' in data

def test_get_dashboard_overview(client):
    """Test getting comprehensive dashboard overview"""
    response = client.get('/api/dashboard/overview')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert 'breath_state' in data
    assert 'glint_stats' in data
    assert 'ritual_stats' in data
    assert 'system_health' in data

def test_dashboard_stream_headers(client):
    """Test dashboard stream headers"""
    response = client.get('/api/dashboard/stream')
    assert response.status_code == 200
    assert response.mimetype == 'text/event-stream'
    assert 'Cache-Control' in response.headers
    assert 'Connection' in response.headers

def test_breath_state_update():
    """Test breath state update function"""
    from routes.dashboard_api import update_breath_state
    
    # Store original state
    original_state = DASHBOARD_DATA['breath_state'].copy()
    
    # Update state
    update_breath_state()
    
    # Verify state was updated
    assert DASHBOARD_DATA['breath_state']['last_update'] != original_state['last_update']
    assert 'phase' in DASHBOARD_DATA['breath_state']
    assert 'progress' in DASHBOARD_DATA['breath_state']
    assert 'climate' in DASHBOARD_DATA['breath_state']

if __name__ == '__main__':
    pytest.main([__file__])
