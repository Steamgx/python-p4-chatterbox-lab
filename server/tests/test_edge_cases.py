import pytest
from app import app
from models import db, Message

def test_invalid_message_creation(client):
    """Test creating message with invalid data"""
    # Missing required fields
    with app.app_context():
        response = client.post(
            '/messages',
            data='{"invalid": "data"}',
            content_type='application/json'
        )
        assert response.status_code == 400

def test_nonexistent_message_operations(client):
    """Test operations on non-existent message"""
    # GET non-existent message
    response = client.get('/messages/9999')
    assert response.status_code == 404

    # PATCH non-existent message
    response = client.patch(
        '/messages/9999',
        data='{"body": "updated"}',
        content_type='application/json'
    )
    assert response.status_code == 404

    # DELETE non-existent message
    response = client.delete('/messages/9999')
    assert response.status_code == 404

def test_invalid_message_update(client):
    """Test invalid message updates"""
    with app.app_context():
        # Create test message first
        test_msg = Message(body="test", username="tester")
        db.session.add(test_msg)
        db.session.commit()
        
        # Test missing body field
        response = client.patch(
            f'/messages/{test_msg.id}',
            json={"invalid": "data"},
            content_type='application/json'
        )
        assert response.status_code == 400
        assert b"must include 'body'" in response.data

        # Test empty data
        response = client.patch(
            f'/messages/{test_msg.id}',
            json={},
            content_type='application/json'
        )
        assert response.status_code == 400

        # Clean up
        db.session.delete(test_msg)
        db.session.commit()
