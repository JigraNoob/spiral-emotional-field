import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_test_init(client):
    response = client.get('/test_init')
    assert response.status_code == 200

def test_resonance_memory(client):
    response = client.get('/resonance/memory')
    assert response.status_code == 200

def test_ritual_invitations(client):
    response = client.get('/ritual/invitations')
    assert response.status_code == 200

def test_get_encounters(client):
    response = client.get('/get/encounters')
    assert response.status_code == 200
