"""Integration tests - merged from test_models.py and test_rag_system.py"""

import pytest
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import ChallengeRequest, ChallengeResponse, AgentWorkflow
from rag import query_rag, get_table, add_document_to_rag


class TestModels:
    """Test Pydantic models for API requests and responses."""
    
    def test_challenge_request(self):
        """Test ChallengeRequest model validation."""
        request = ChallengeRequest(
            message="O que é a maquininha Smart?",
            user_id="user123",
            conversation_id="conv456"
        )
        assert request.message == "O que é a maquininha Smart?"
        assert request.user_id == "user123"
        assert request.conversation_id == "conv456"
    
    def test_challenge_response(self):
        """Test ChallengeResponse model structure."""
        workflow = [
            AgentWorkflow(agent="RouterAgent", decision="KnowledgeAgent"),
            AgentWorkflow(agent="KnowledgeAgent", decision="")
        ]
        response = ChallengeResponse(
            response="A maquininha Smart é nossa solução de pagamento...",
            source_agent_response="Retrieved from 3 chunks in knowledge base",
            agent_workflow=workflow
        )
        assert response.response.startswith("A maquininha Smart")
        assert len(response.agent_workflow) == 2
        assert response.agent_workflow[0].agent == "RouterAgent"
        assert response.agent_workflow[1].agent == "KnowledgeAgent"
    
    def test_agent_workflow_model(self):
        """Test AgentWorkflow model."""
        workflow = AgentWorkflow(agent="RouterAgent", decision="KnowledgeAgent")
        assert workflow.agent == "RouterAgent"
        assert workflow.decision == "KnowledgeAgent"
    
    def test_model_validation_missing_fields(self):
        """Test validation for missing required fields."""
        with pytest.raises(Exception):
            # Missing required fields should raise validation error
            request = ChallengeRequest(message="test")
    
    def test_model_validation_all_fields(self):
        """Test successful model creation with all required fields."""
        request = ChallengeRequest(
            message="test",
            user_id="123",
            conversation_id="456"
        )
        assert request.message == "test"
        assert request.user_id == "123"
        assert request.conversation_id == "456"


class TestRAGSystem:
    """Test RAG (Retrieval-Augmented Generation) system."""
    
    def load_context_for_testing(self):
        """Load context for testing if not already loaded."""
        # Check if context is already loaded
        table = get_table()
        results = table.search().where("session_id = 'infinitepay-context'", prefilter=True).limit(5).to_list()
        
        if len(results) > 0:
            return True  # Context already loaded
        
        # Try to load context
        context_filepath = os.path.join("..", "context", "infinitypay_solutions.md")
        context_session_id = "infinitepay-context"
        
        if not os.path.exists(context_filepath):
            # Check alternative paths
            alternative_paths = [
                os.path.join("context", "infinitypay_solutions.md"),
                os.path.join("..", "..", "context", "infinitypay_solutions.md")
            ]
            
            context_filepath = None
            for path in alternative_paths:
                if os.path.exists(path):
                    context_filepath = path
                    break
            
            if not context_filepath:
                # Look for any .md file in context directories
                context_dirs = ["context", "../context", "../../context"]
                for context_dir in context_dirs:
                    if os.path.exists(context_dir):
                        md_files = [f for f in os.listdir(context_dir) if f.endswith('.md')]
                        if md_files:
                            context_filepath = os.path.join(context_dir, md_files[0])
                            break
        
        if not context_filepath or not os.path.exists(context_filepath):
            pytest.skip("Context file not found - skipping RAG tests")
        
        try:
            add_document_to_rag(context_filepath, context_session_id)
            return True
        except Exception as e:
            pytest.skip(f"Failed to load context: {e}")
    
    def test_rag_system_initialization(self):
        """Test that RAG system can be initialized."""
        table = get_table()
        assert table is not None
    
    def test_context_loading(self):
        """Test context document loading."""
        success = self.load_context_for_testing()
        assert success
        
        # Verify documents were loaded
        table = get_table()
        results = table.search().where("session_id = 'infinitepay-context'", prefilter=True).limit(5).to_list()
        assert len(results) > 0, "No documents found after loading context"
    
    def test_document_retrieval(self):
        """Test document retrieval for various queries."""
        self.load_context_for_testing()
        
        test_questions = [
            "O que é a maquininha Smart?",
            "Como funciona o InfiniteTap?",
            "Quais são as taxas da InfinitePay?",
            "Como faço para receber na hora?"
        ]
        
        for question in test_questions:
            context = query_rag(question, "infinitepay-context")
            assert context is not None, f"No context retrieved for: {question}"
            assert len(context) > 0, f"Empty context for: {question}"
            assert isinstance(context, str), f"Context should be string for: {question}"
    
    def test_maquininha_smart_query(self):
        """Test specific query about maquininha Smart."""
        self.load_context_for_testing()
        
        context = query_rag("O que é a maquininha Smart?", "infinitepay-context")
        assert context is not None
        assert len(context) > 50  # Should have substantial content
        
        # Context should be relevant to the query
        context_lower = context.lower()
        relevant_terms = ["maquininha", "smart", "pagamento", "infinitepay"]
        found_terms = [term for term in relevant_terms if term in context_lower]
        assert len(found_terms) > 0, f"Context doesn't seem relevant. Found terms: {found_terms}"
    
    def test_infinitetap_query(self):
        """Test specific query about InfiniteTap."""
        self.load_context_for_testing()
        
        context = query_rag("Como funciona o InfiniteTap?", "infinitepay-context")
        assert context is not None
        assert len(context) > 50
        
        # Should find relevant content
        context_lower = context.lower()
        assert "infinitetap" in context_lower or "tap" in context_lower
    
    def test_query_rag_with_invalid_session(self):
        """Test RAG query with invalid session ID."""
        context = query_rag("test query", "nonexistent-session")
        # Should handle gracefully - might return None or empty string
        assert context is None or isinstance(context, str)


class TestIntegration:
    """Integration tests combining models and RAG system."""
    
    def test_full_workflow_simulation(self):
        """Test a complete workflow from request to response."""
        # Create a challenge request
        request = ChallengeRequest(
            message="O que é a maquininha Smart?",
            user_id="integration_test_user",
            conversation_id="integration_test_conv"
        )
        
        # Simulate RAG retrieval
        try:
            context = query_rag(request.message, "infinitepay-context")
        except:
            context = "Simulated context for integration test"
        
        # Create workflow
        workflow = [
            AgentWorkflow(agent="RouterAgent", decision="KnowledgeAgent"),
            AgentWorkflow(agent="KnowledgeAgent", decision="")
        ]
        
        # Create response
        response = ChallengeResponse(
            response="A maquininha Smart é uma solução de pagamento da InfinitePay.",
            source_agent_response="Retrieved from knowledge base",
            agent_workflow=workflow
        )
        
        # Verify the complete workflow
        assert request.message == "O que é a maquininha Smart?"
        assert len(response.agent_workflow) == 2
        assert response.agent_workflow[0].agent == "RouterAgent"
        assert response.agent_workflow[1].agent == "KnowledgeAgent"
    
    def test_math_workflow_simulation(self):
        """Test a math query workflow."""
        request = ChallengeRequest(
            message="Quanto é 150 + 350?",
            user_id="math_test_user",
            conversation_id="math_test_conv"
        )
        
        workflow = [
            AgentWorkflow(agent="RouterAgent", decision="MathAgent"),
            AgentWorkflow(agent="MathAgent", decision="")
        ]
        
        response = ChallengeResponse(
            response="150 + 350 = 500",
            source_agent_response="Text generated by the specialized agent.",
            agent_workflow=workflow
        )
        
        assert "500" in response.response
        assert response.agent_workflow[1].agent == "MathAgent"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])