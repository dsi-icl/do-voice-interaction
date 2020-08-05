import falcon
from falcon import testing
import pytest
import json
from urllib.parse import urlencode

from do_control_service.doapi.app import api

@pytest.fixture
def client():
    return testing.TestClient(api)

def test_status(client):
    
    response = client.simulate_get('/api/status')
    assert response.text == 'Service is running'
    assert response.status == falcon.HTTP_200

def test_json(client):

    response = client.simulate_get('/api/json')
    assert response.text == '{"data": "sampleData"}'
    assert response.status == falcon.HTTP_200

def test_chatbot(client):

    response = client.simulate_post('/api/chatbot',body='{"message":"Hello"}')
    result = response.json[0]
    assert result["text"] == "Welcome to the Data Observatory. I am your voice assistant. Can I help you ?"
    assert response.status == falcon.HTTP_OK

    response = client.simulate_post('/api/chatbot',body='{"message":"Bye"}')
    result = response.json[0]
    assert result["text"] == "The Data Observatory thanks you for your presentation. I hope to see you soon :)"
    assert response.status == falcon.HTTP_OK

