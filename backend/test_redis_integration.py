import requests
import time
from redis_client import redis_client

# Make a request
response = requests.post("http://localhost:8000/chat", json={
    "message": "O que é Pix?",
    "user_id": "test",
    "conversation_id": "redis_test_123"
})

# Check Redis for the conversation
time.sleep(1)
conversation = redis_client.get_conversation("redis_test_123")
print(f"Conversation in Redis: {len(conversation)} messages")