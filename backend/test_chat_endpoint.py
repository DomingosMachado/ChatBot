import requests
import json

def test_chat_endpoint():
    """
    Test the challenge-compliant /chat endpoint
    """
    base_url = "http://localhost:8000"
    
    test_cases = [
        {
            "name": "Knowledge Query",
            "payload": {
                "message": "O que é a maquininha Smart?",
                "user_id": "test_user_001",
                "conversation_id": "test_conv_001"
            },
            "expected_agent": "KnowledgeAgent"
        },
        {
            "name": "Math Query",
            "payload": {
                "message": "Quanto é 25 + 37?",
                "user_id": "test_user_002",
                "conversation_id": "test_conv_002"
            },
            "expected_agent": "MathAgent"
        },
        {
            "name": "InfinitePay Feature Query",
            "payload": {
                "message": "Como funciona o InfiniteTap?",
                "user_id": "test_user_003",
                "conversation_id": "test_conv_003"
            },
            "expected_agent": "KnowledgeAgent"
        }
    ]
    
    for test in test_cases:
        print(f"\n📝 Testing: {test['name']}")
        print(f"   Payload: {test['payload']['message']}")
        
        try:
            response = requests.post(
                f"{base_url}/chat",
                json=test['payload'],
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                
                assert "response" in data, "Missing 'response' field"
                assert "source_agent_response" in data, "Missing 'source_agent_response' field"
                assert "agent_workflow" in data, "Missing 'agent_workflow' field"
                assert isinstance(data["agent_workflow"], list), "agent_workflow must be a list"
                assert len(data["agent_workflow"]) >= 2, "agent_workflow must have at least 2 steps"
                
                assert data["agent_workflow"][0]["agent"] == "RouterAgent", "First agent must be RouterAgent"
                assert data["agent_workflow"][1]["agent"] == test["expected_agent"], f"Second agent should be {test['expected_agent']}"
                
                print(f"   ✅ Response structure correct")
                print(f"   ✅ Agent workflow: {[w['agent'] for w in data['agent_workflow']]}")
                print(f"   ✅ Response preview: {data['response'][:100]}...")
                print(f"   ✅ Source: {data['source_agent_response']}")
                
            else:
                print(f"   ❌ Failed with status {response.status_code}")
                print(f"   Error: {response.text}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print("\n" + "="*50)
    print("📊 Testing complete format compliance...")
    
    sample_request = {
        "message": "teste",
        "user_id": "123",
        "conversation_id": "456"
    }
    
    response = requests.post(f"{base_url}/chat", json=sample_request)
    if response.status_code == 200:
        print("✅ API endpoint accepts correct format")
        print(f"✅ Response JSON structure:\n{json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    else:
        print(f"❌ API failed: {response.status_code}")

if __name__ == "__main__":
    print("🚀 Starting API tests...")
    print("⚠️  Make sure the server is running: uvicorn app:app --reload")
    input("Press Enter when server is ready...")
    test_chat_endpoint()