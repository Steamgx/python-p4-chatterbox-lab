import json
import pytest
from datetime import datetime, timedelta

def test_get_messages(client):
    """Test GET /messages endpoint returns all messages"""
    response = client.get('/messages')
    assert response.status_code == 200
    
    messages = json.loads(response.data)
    assert len(messages) == 3  # From our fixture data
    assert all(isinstance(msg['id'], int) for msg in messages)
    assert all('body' in msg for msg in messages)
    assert all('username' in msg for msg in messages)
    assert all('created_at' in msg for msg in messages)

def test_create_message(client, message_data):
    """Test POST /messages creates new message"""
    response = client.post(
        '/messages',
        data=json.dumps(message_data),
        content_type='application/json'
    )
    assert response.status_code == 201
    
    created_message = json.loads(response.data)
    assert created_message['body'] == message_data['body']
    assert created_message['username'] == message_data['username']
    assert isinstance(created_message['id'], int)

def test_get_single_message(client):
    """Test GET /messages/<id> returns specific message"""
    # Get ID from existing messages
    messages = json.loads(client.get('/messages').data)
    test_id = messages[0]['id']
    
    response = client.get(f'/messages/{test_id}')
    assert response.status_code == 200
    
    message = json.loads(response.data)
    assert message['id'] == test_id
    assert 'body' in message
    assert 'username' in message

def test_update_message(client):
    """Test PATCH /messages/<id> updates message"""
    messages = json.loads(client.get('/messages').data)
    test_id = messages[0]['id']
    update_data = {'body': 'Updated message content'}
    
    response = client.patch(
        f'/messages/{test_id}',
        data=json.dumps(update_data),
        content_type='application/json'
    )
    assert response.status_code == 200
    
    updated_message = json.loads(response.data)
    assert updated_message['body'] == update_data['body']
    assert updated_message['id'] == test_id

def test_delete_message(client):
    """Test DELETE /messages/<id> removes message"""
    messages = json.loads(client.get('/messages').data)
    test_id = messages[0]['id']
    
    response = client.delete(f'/messages/{test_id}')
    assert response.status_code == 204
    
    # Verify deletion
    response = client.get(f'/messages/{test_id}')
    assert response.status_code == 404
