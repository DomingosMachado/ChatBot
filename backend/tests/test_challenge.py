"""Challenge endpoint tests - merged from test_chat_endpoint.py and test_complete_system.py"""

import pytest
import requests
import json
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

class TestChallengeEndpoint:
    """Test the /chat endpoint for challenge compliance."""
    
    def test_knowledge_query_routing(self):
        """Test knowledge base query returns correct format."""
        response = client.post("/chat", json={
            "message": "O que é a maquininha Smart?",
            "user_id": "test_user_001",
            "conversation_id": "test_conv_001"
        })
        
        assert response.status_code == 200
        data = response.json()
        
        assert "response" in data, "Missing 'response' field"
        assert "source_agent_response" in data, "Missing 'source_agent_response' field"
        assert "agent_workflow" in data, "Missing 'agent_workflow' field"
        assert isinstance(data["agent_workflow"], list), "agent_workflow must be a list"
        assert len(data["agent_workflow"]) >= 2, "agent_workflow must have at least 2 steps"
        
        assert data["agent_workflow"][0]["agent"] == "RouterAgent", "First agent must be RouterAgent"
        assert data["agent_workflow"][1]["agent"] == "KnowledgeAgent", "Second agent should be KnowledgeAgent"
    
    def test_math_query_routing(self):
        """Test math query returns correct format."""
        response = client.post("/chat", json={
            "message": "Quanto é 25 + 37?",
            "user_id": "test_user_002",
            "conversation_id": "test_conv_002"
        })
        
        assert response.status_code == 200
        data = response.json()
        
        assert "response" in data
        assert "62" in data["response"]
        assert data["agent_workflow"][1]["agent"] == "MathAgent"
    
    def test_infinitepay_feature_query(self):
        """Test InfinitePay feature query routing."""
        response = client.post("/chat", json={
            "message": "Como funciona o InfiniteTap?",
            "user_id": "test_user_003",
            "conversation_id": "test_conv_003"
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["agent_workflow"][1]["agent"] == "KnowledgeAgent"
    
    def test_missing_required_field(self):
        """Test validation for missing required fields."""
        response = client.post("/chat", json={
            "message": "teste",
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
    
    def test_correct_request_format(self):
        """Test API accepts correct challenge format."""
        response = client.post("/chat", json={
            "message": "teste",
            "user_id": "user_123",
            "conversation_id": "conv_456"
        })
        
        assert response.status_code == 200
        data = response.json()
        
        # Check all required fields are present
        required_fields = ["response", "source_agent_response", "agent_workflow"]
        for field in required_fields:
            assert field in data, f"Missing required field: {field}"

class TestKnowledgeBase:
    """Test knowledge base functionality."""
    
    def test_infinitepay_pix_query(self):
        """Test InfinitePay Pix query returns relevant information."""
        response = client.post("/chat", json={
            "message": "Como funciona o Pix da InfinitePay?",
            "user_id": "test_user",
            "conversation_id": "test_conv_3"
        })
        
        assert response.status_code == 200
        data = response.json()
        
        # Check for expected keywords in response
        response_text = data["response"].lower()
        expected_keywords = ["pix", "infinitepay"]
        for keyword in expected_keywords:
            assert keyword in response_text, f"Missing keyword: {keyword}"
    
    def test_source_attribution(self):
        """Test that knowledge base responses include source attribution."""
        response = client.post("/chat", json={
            "message": "O que é o InfiniteTap?",
            "user_id": "test_user", 
            "conversation_id": "test_conv_4"
        })
        
        assert response.status_code == 200
        data = response.json()
        
        # Check source attribution is present
        source_info = data["source_agent_response"].lower()
        assert "knowledge base" in source_info or "retrieved" in source_info

class TestMathOperations:
    """Test math operations functionality."""
    
    def test_addition(self):
        """Test basic addition."""
        response = client.post("/chat", json={
            "message": "25 + 75",
            "user_id": "test_user",
            "conversation_id": "test_conv_5"
        })
        
        assert response.status_code == 200
        data = response.json()
        assert "100" in data["response"]
        assert data["agent_workflow"][1]["agent"] == "MathAgent"
    
    def test_percentage_calculation(self):
        """Test percentage calculation."""
        response = client.post("/chat", json={
            "message": "20% de 500",
            "user_id": "test_user",
            "conversation_id": "test_conv_6"
        })
        
        assert response.status_code == 200
        data = response.json()
        assert "100" in data["response"]
        assert data["agent_workflow"][1]["agent"] == "MathAgent"
    
    def test_complex_math(self):
        """Test more complex math operation."""
        response = client.post("/chat", json={
            "message": "Quanto é 150 + 350?",
            "user_id": "test_user",
            "conversation_id": "test_conv_complex"
        })
        
        assert response.status_code == 200
        data = response.json()
        assert "500" in data["response"]

class TestAgentWorkflow:
    """Test agent workflow structure."""
    
    def test_router_always_first(self):
        """Test that RouterAgent is always first in workflow."""
        test_cases = [
            {"message": "O que é InfinitePay?", "user_id": "test", "conversation_id": "test1"},
            {"message": "2 + 2", "user_id": "test", "conversation_id": "test2"}
        ]
        
        for case in test_cases:
            response = client.post("/chat", json=case)
            assert response.status_code == 200
            data = response.json()
            assert data["agent_workflow"][0]["agent"] == "RouterAgent"
    
    def test_workflow_structure(self):
        """Test that workflow has correct structure."""
        response = client.post("/chat", json={
            "message": "teste",
            "user_id": "test_user",
            "conversation_id": "test_workflow"
        })
        
        assert response.status_code == 200
        data = response.json()
        
        workflow = data["agent_workflow"]
        assert len(workflow) >= 2
        for step in workflow:
            assert "agent" in step
            assert "decision" in step

if __name__ == "__main__":
    pytest.main([__file__, "-v"])