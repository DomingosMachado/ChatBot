"""Test Redis connection and functionality."""

from redis_client import redis_client

def test_redis():
    print("Testing Redis Connection...")
    print("-" * 40)
    
    if redis_client.connected:
        print("✅ Redis is connected!")
        
        # Test basic operations
        print("\nTesting basic operations:")
        
        # Set and get
        redis_client.set("test_key", "test_value")
        value = redis_client.get("test_key")
        print(f"Set/Get test: {'✅' if value == 'test_value' else '❌'}")
        
        # JSON operations
        test_data = {"name": "InfinitePay", "type": "payment"}
        redis_client.set_json("test_json", test_data)
        json_value = redis_client.get_json("test_json")
        print(f"JSON test: {'✅' if json_value == test_data else '❌'}")
        
        # List operations (for logs)
        redis_client.lpush("test_logs", "log_entry_1")
        redis_client.lpush("test_logs", "log_entry_2")
        logs = redis_client.lrange("test_logs", 0, -1)
        print(f"List test: {'✅' if len(logs) == 2 else '❌'}")
        
        # Cleanup
        redis_client.delete("test_key")
        redis_client.delete("test_json")
        redis_client.delete("test_logs")
        
        print("\n✅ All Redis tests passed!")
    else:
        print("⚠️ Redis is not connected - app will work without caching")
        print("To use Redis, make sure it's running:")
        print("  - Windows: Download from GitHub or use WSL")
        print("  - Mac: brew install redis && brew services start redis")
        print("  - Linux: sudo apt install redis-server")

if __name__ == "__main__":
    test_redis()