"""Unit tests for CloudWalk Chat API."""

import pytest
import json
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

class TestChallengeEndpoint:
    """Test the /chat endpoint for challenge compliance."""
    
    def test_valid_knowledge_query(self):
        """Test knowledge base query returns correct format."""
        response = client.post("/chat", json={
            "message": "O que é o Pix da InfinitePay?",
            "user_id": "test_user",
            "conversation_id": "test_conv_1"
        })
        
        assert response.status_code == 200
        data = response.json()
        
        assert "response" in data
        assert "source_agent_response" in data
        assert "agent_workflow" in data
        assert len(data["agent_workflow"]) == 2
        assert data["agent_workflow"][0]["agent"] == "RouterAgent"
        assert data["agent_workflow"][1]["agent"] == "KnowledgeAgent"
    
    def test_valid_math_query(self):
        """Test math query returns correct format."""
        response = client.post("/chat", json={
            "message": "Quanto é 150 + 350?",
            "user_id": "test_user",
            "conversation_id": "test_conv_2"
        })
        
        assert response.status_code == 200
        data = response.json()
        
        assert "response" in data
        assert "500" in data["response"]
        assert data["agent_workflow"][1]["agent"] == "MathAgent"
    
    def test_missing_required_field(self):
        """Test validation for missing required fields."""
        response = client.post("/chat", json={
            "message": "test",
            "user_id": "test_user"
        })
        
        assert response.status_code == 422
    
    def test_empty_message(self):
        """Test validation for empty message."""
        response = client.post("/chat", json={
            "message": "",
            "user_id": "test_user",
            "conversation_id": "test_conv"
        })
        
        assert response.status_code == 422
    
    def test_sanitization(self):
        """Test input sanitization."""
        response = client.post("/chat", json={
            "message": "What is <script>alert('xss')</script> InfinitePay?",
            "user_id": "test_user",
            "conversation_id": "test_conv_3"
        })
        
        assert response.status_code == 200
        data = response.json()
        assert "<script>" not in data["response"]

class TestHistoryEndpoint:
    """Test conversation history endpoints."""
    
    def test_get_history(self):
        """Test retrieving conversation history."""
        session_id = "test_session_history"
        
        client.post("/chat", json={
            "message": "Test message",
            "user_id": "test_user",
            "conversation_id": session_id
        })
        
        response = client.get(f"/api/history/{session_id}")
        assert response.status_code == 200
        
        data = response.json()
        assert "session_id" in data
        assert "messages" in data
        assert len(data["messages"]) >= 2
    
    def test_invalid_session_id(self):
        """Test invalid session ID format."""
        response = client.get("/api/history/invalid-session-!@#")
        assert response.status_code == 400

class TestAnalyticsEndpoint:
    """Test analytics endpoints."""
    
    def test_get_analytics(self):
        """Test analytics endpoint returns correct structure."""
        response = client.get("/api/analytics")
        assert response.status_code == 200
        
        data = response.json()
        if data.get("total_interactions", 0) > 0:
            assert "agent_usage" in data
            assert "average_execution_time" in data
            assert "math" in data["agent_usage"]
            assert "knowledge" in data["agent_usage"]

class TestHealthCheck:
    """Test health check endpoint."""
    
    def test_health_endpoint(self):
        """Test health check returns correct status."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data

if __name__ == "__main__":
    pytest.main([__file__, "-v"])