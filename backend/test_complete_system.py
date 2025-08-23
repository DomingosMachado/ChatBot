import requests
import json
import time

def test_complete_system():
    """
    Comprehensive test of the complete CloudWalk challenge system
    """
    base_url = "http://localhost:8000"
    
    print("🚀 CloudWalk Challenge - Complete System Test")
    print("=" * 60)
    
    test_scenarios = [
        {
            "category": "API CONTRACT",
            "tests": [
                {
                    "name": "Correct Request Format",
                    "payload": {
                        "message": "teste",
                        "user_id": "user_123",
                        "conversation_id": "conv_456"
                    },
                    "check_fields": ["response", "source_agent_response", "agent_workflow"]
                },
                {
                    "name": "Missing Fields Rejection",
                    "payload": {"message": "teste"},
                    "expect_error": True
                }
            ]
        },
        {
            "category": "AGENT ROUTING",
            "tests": [
                {
                    "name": "Knowledge Query Routing",
                    "payload": {
                        "message": "O que é a maquininha Smart?",
                        "user_id": "test_user",
                        "conversation_id": "test_conv_1"
                    },
                    "expected_agent": "KnowledgeAgent"
                },
                {
                    "name": "Math Query Routing",
                    "payload": {
                        "message": "Quanto é 150 + 350?",
                        "user_id": "test_user",
                        "conversation_id": "test_conv_2"
                    },
                    "expected_agent": "MathAgent"
                }
            ]
        },
        {
            "category": "KNOWLEDGE BASE",
            "tests": [
                {
                    "name": "InfinitePay Features",
                    "payload": {
                        "message": "Como funciona o Pix da InfinitePay?",
                        "user_id": "test_user",
                        "conversation_id": "test_conv_3"
                    },
                    "expected_keywords": ["Pix", "InfinitePay"]
                },
                {
                    "name": "Source Attribution",
                    "payload": {
                        "message": "O que é o InfiniteTap?",
                        "user_id": "test_user",
                        "conversation_id": "test_conv_4"
                    },
                    "check_source": True
                }
            ]
        },
        {
            "category": "MATH OPERATIONS",
            "tests": [
                {
                    "name": "Addition",
                    "payload": {
                        "message": "25 + 75",
                        "user_id": "test_user",
                        "conversation_id": "test_conv_5"
                    },
                    "expected_result": "100"
                },
                {
                    "name": "Percentage",
                    "payload": {
                        "message": "20% de 500",
                        "user_id": "test_user",
                        "conversation_id": "test_conv_6"
                    },
                    "expected_result": "100"
                }
            ]
        }
    ]
    
    passed = 0
    failed = 0
    
    for category in test_scenarios:
        print(f"\n📋 {category['category']}")
        print("-" * 40)
        
        for test in category["tests"]:
            try:
                response = requests.post(
                    f"{base_url}/chat",
                    json=test["payload"],
                    headers={"Content-Type": "application/json"}
                )
                
                if test.get("expect_error"):
                    if response.status_code == 422:
                        print(f"✅ {test['name']}: Correctly rejected invalid request")
                        passed += 1
                    else:
                        print(f"❌ {test['name']}: Should have rejected but got {response.status_code}")
                        failed += 1
                    continue
                
                if response.status_code != 200:
                    print(f"❌ {test['name']}: HTTP {response.status_code}")
                    failed += 1
                    continue
                
                data = response.json()
                
                if test.get("check_fields"):
                    missing = [f for f in test["check_fields"] if f not in data]
                    if missing:
                        print(f"❌ {test['name']}: Missing fields {missing}")
                        failed += 1
                        continue
                
                if test.get("expected_agent"):
                    actual_agent = data["agent_workflow"][1]["agent"]
                    if actual_agent != test["expected_agent"]:
                        print(f"❌ {test['name']}: Expected {test['expected_agent']}, got {actual_agent}")
                        failed += 1
                        continue
                
                if test.get("expected_keywords"):
                    missing_keywords = [k for k in test["expected_keywords"] 
                                       if k.lower() not in data["response"].lower()]
                    if missing_keywords:
                        print(f"❌ {test['name']}: Missing keywords {missing_keywords}")
                        failed += 1
                        continue
                
                if test.get("check_source"):
                    if "knowledge base" not in data["source_agent_response"].lower():
                        print(f"❌ {test['name']}: Source not properly attributed")
                        failed += 1
                        continue
                
                if test.get("expected_result"):
                    if test["expected_result"] not in data["response"]:
                        print(f"❌ {test['name']}: Expected {test['expected_result']} in response")
                        failed += 1
                        continue
                
                print(f"✅ {test['name']}: PASSED")
                passed += 1
                
            except Exception as e:
                print(f"❌ {test['name']}: Error - {str(e)}")
                failed += 1
    
    print("\n" + "=" * 60)
    print("📊 FINAL RESULTS")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"📈 Success Rate: {(passed/(passed+failed)*100):.1f}%")
    
    if failed == 0:
        print("\n🎉 ALL TESTS PASSED! System is ready for CloudWalk challenge!")
    else:
        print("\n⚠️  Some tests failed. Review and fix before submission.")
    
    print("\n📝 LOGGING CHECK")
    logs_response = requests.get(f"{base_url}/api/logs/recent?limit=5")
    if logs_response.status_code == 200:
        logs = logs_response.json()
        print(f"✅ Recent logs available: {logs['total']} entries")
    
    print("\n🔍 PERFORMANCE METRICS")
    analytics_response = requests.get(f"{base_url}/api/analytics")
    if analytics_response.status_code == 200:
        analytics = analytics_response.json()
        if analytics.get("total_interactions", 0) > 0:
            print(f"✅ Total interactions: {analytics['total_interactions']}")
            print(f"✅ Avg execution time (Knowledge): {analytics['average_execution_time']['knowledge']:.3f}s")
            print(f"✅ Avg execution time (Math): {analytics['average_execution_time']['math']:.3f}s")

if __name__ == "__main__":
    print("⚠️  Make sure the server is running: uvicorn app:app --reload")
    input("Press Enter when ready...")
    test_complete_system()