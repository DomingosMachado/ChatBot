"""Input validation for API requests."""

import re
import html
from typing import Optional
from pydantic import BaseModel, Field, field_validator

class ChallengeRequestValidator(BaseModel):
    """Validates challenge endpoint requests."""
    
    message: str = Field(..., min_length=1, max_length=1000)
    user_id: str = Field(..., min_length=1, max_length=100)
    conversation_id: str = Field(..., min_length=1, max_length=100)
    
    @field_validator('message')
    def validate_message(cls, v):
        v = v.strip()
        if not v:
            raise ValueError("Message cannot be empty")
        if len(v) > 1000:
            raise ValueError("Message too long (max 1000 characters)")
        return v
    
    @field_validator('user_id', 'conversation_id')
    def validate_ids(cls, v):
        if not re.match(r'^[a-zA-Z0-9_-]+$', v):
            raise ValueError("ID must contain only alphanumeric characters, hyphens, and underscores")
        return v

class QueryValidator:
    """Validates and sanitizes user queries."""
    
    MAX_QUERY_LENGTH = 1000
    MAX_MATH_EXPRESSION_LENGTH = 100
    
    @staticmethod
    def sanitize_query(query: str) -> str:
        """Remove potentially harmful characters while preserving math symbols."""
        if not query:
            return ""
        
        query = query.strip()
        query = html.escape(query)
        
        query = re.sub(r'[<>\"\'`;]', '', query)
        
        query = re.sub(r'\s+', ' ', query)
        
        if len(query) > QueryValidator.MAX_QUERY_LENGTH:
            query = query[:QueryValidator.MAX_QUERY_LENGTH]
        
        return query
    
    @staticmethod
    def check_prompt_injection(query: str) -> bool:
        """Check for prompt injection attempts."""
        dangerous_patterns = [
            'ignore previous', 'forget everything', 'system prompt',
            'reveal your', 'jailbreak', 'developer mode', 'act as admin'
        ]
        query_lower = query.lower()
        for pattern in dangerous_patterns:
            if pattern in query_lower:
                return False
        return True
    
    @staticmethod
    def validate_math_expression(expression: str) -> bool:
        """Check if math expression is safe to evaluate."""
        if len(expression) > QueryValidator.MAX_MATH_EXPRESSION_LENGTH:
            return False
        
        allowed_chars = set('0123456789+-*/().,%^ ')
        if not all(c in allowed_chars for c in expression):
            return False
        
        if expression.count('(') != expression.count(')'):
            return False
        
        return True
    
    @staticmethod
    def validate_session_id(session_id: str) -> bool:
        """Validate session ID format."""
        if not session_id:
            return False
        
        if len(session_id) > 100:
            return False
        
        if not re.match(r'^[a-zA-Z0-9_-]+$', session_id):
            return False
        
        return True

class ResponseValidator:
    """Validates agent responses before sending to client."""
    
    @staticmethod
    def validate_response(response: str) -> str:
        """Ensure response is safe and well-formed."""
        if not response:
            return "Desculpe, não consegui processar sua solicitação."
        
        if len(response) > 5000:
            response = response[:4997] + "..."
        
        response = response.strip()
        
        return response
    
    @staticmethod
    def validate_workflow(workflow: list) -> bool:
        """Validate agent workflow structure."""
        if not workflow or len(workflow) < 2:
            return False
        
        if workflow[0].get('agent') != 'RouterAgent':
            return False
        
        valid_agents = {'RouterAgent', 'KnowledgeAgent', 'MathAgent'}
        for step in workflow:
            if step.get('agent') not in valid_agents:
                return False
        
        return True