"""Redis client for caching and session management."""

import redis
import json
import os
from typing import Optional, Any
from dotenv import load_dotenv

load_dotenv()

class RedisClient:
    """Redis client with fallback to work without Redis."""
    
    def __init__(self):
        self.redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
        self.client = None
        self.connected = False
        
        try:
            # Support for Redis Cloud with SSL
            if self.redis_url.startswith("rediss://"):
                self.client = redis.from_url(self.redis_url, decode_responses=True, ssl_cert_reqs=None)
            else:
                self.client = redis.from_url(self.redis_url, decode_responses=True)
            
            self.client.ping()
            self.connected = True
            print("✅ Redis connected successfully")
        except (redis.ConnectionError, redis.RedisError) as e:
            print(f"⚠️ Redis not available, using fallback mode: {e}")
            self.connected = False
    
    def get(self, key: str) -> Optional[str]:
        """Get value from Redis, returns None if not connected."""
        if not self.connected:
            return None
        try:
            return self.client.get(key)
        except:
            return None
    
    def set(self, key: str, value: str, ex: int = 3600) -> bool:
        """Set value in Redis with expiration, returns False if not connected."""
        if not self.connected:
            return False
        try:
            self.client.set(key, value, ex=ex)
            return True
        except:
            return False
    
    def get_json(self, key: str) -> Optional[dict]:
        """Get JSON value from Redis."""
        value = self.get(key)
        if value:
            try:
                return json.loads(value)
            except:
                return None
        return None
    
    def set_json(self, key: str, value: dict, ex: int = 3600) -> bool:
        """Set JSON value in Redis."""
        try:
            json_str = json.dumps(value)
            return self.set(key, json_str, ex)
        except:
            return False
    
    def delete(self, key: str) -> bool:
        """Delete key from Redis."""
        if not self.connected:
            return False
        try:
            self.client.delete(key)
            return True
        except:
            return False
    
    def exists(self, key: str) -> bool:
        """Check if key exists in Redis."""
        if not self.connected:
            return False
        try:
            return self.client.exists(key) > 0
        except:
            return False
    
    def lpush(self, key: str, value: str) -> bool:
        """Push value to Redis list (for logs)."""
        if not self.connected:
            return False
        try:
            self.client.lpush(key, value)
            self.client.ltrim(key, 0, 99)  # Keep only last 100 items
            return True
        except:
            return False
    
    def lrange(self, key: str, start: int = 0, end: int = -1) -> list:
        """Get list from Redis."""
        if not self.connected:
            return []
        try:
            return self.client.lrange(key, start, end)
        except:
            return []
    
    def store_conversation(self, session_id: str, message: dict) -> bool:
        """Store conversation message in Redis."""
        if not self.connected:
            return False
        try:
            key = f"conversation:{session_id}"
            self.lpush(key, json.dumps(message))
            self.client.expire(key, 86400)  # Keep for 24 hours
            return True
        except:
            return False
    
    def get_conversation(self, session_id: str) -> list:
        """Get conversation history from Redis."""
        if not self.connected:
            return []
        try:
            key = f"conversation:{session_id}"
            messages = self.lrange(key, 0, -1)
            return [json.loads(msg) for msg in messages]
        except:
            return []
    
    def cache_response(self, query_hash: str, response: str, ex: int = 3600) -> bool:
        """Cache agent response."""
        key = f"response:{query_hash}"
        return self.set(key, response, ex)
    
    def get_cached_response(self, query_hash: str) -> Optional[str]:
        """Get cached agent response."""
        key = f"response:{query_hash}"
        return self.get(key)

redis_client = RedisClient()