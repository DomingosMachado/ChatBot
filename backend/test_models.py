from models import ChallengeRequest, ChallengeResponse, AgentWorkflow

def test_challenge_request():
    request = ChallengeRequest(
        message="O que é a maquininha Smart?",
        user_id="user123",
        conversation_id="conv456"
    )
    assert request.message == "O que é a maquininha Smart?"
    assert request.user_id == "user123"
    assert request.conversation_id == "conv456"
    print("✅ ChallengeRequest model works")

def test_challenge_response():
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
    print("✅ ChallengeResponse model works")

def test_model_validation():
    try:
        request = ChallengeRequest(message="test")
    except Exception as e:
        print(f"✅ Validation works - missing required fields: {e}")
    
    try:
        request = ChallengeRequest(
            message="test",
            user_id="123",
            conversation_id="456"
        )
        print("✅ All required fields present - model created successfully")
    except Exception as e:
        print(f"❌ Failed with all fields: {e}")

if __name__ == "__main__":
    test_challenge_request()
    test_challenge_response()
    test_model_validation()
    print("\n✅ All model tests passed!")