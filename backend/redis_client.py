"""Redis client for logs and health monitoring with graceful degradation."""

import redis
import json
import os
import time
from typing import Optional, Any
from dotenv import load_dotenv

load_dotenv()

class RedisClient:
    """Redis client with retry logic and graceful fallback for production use."""
    
    def __init__(self):
        self.redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
        self.client = None
        self.connected = False
        self.warning_printed = False
        self.max_retries = 3
        self.base_delay = 0.1  # 100ms base delay for exponential backoff
        
        self._connect_with_retry()
    
    def _connect_with_retry(self):
        """Attempt to connect to Redis with exponential backoff retry logic."""
        for attempt in range(self.max_retries):
            try:
                if self.redis_url.startswith("rediss://"):
                    self.client = redis.from_url(
                        self.redis_url, 
                        decode_responses=True, 
                        ssl_cert_reqs=None,
                        socket_timeout=5,
                        socket_connect_timeout=5
                    )
                else:
                    self.client = redis.from_url(
                        self.redis_url, 
                        decode_responses=True,
                        socket_timeout=5,
                        socket_connect_timeout=5
                    )
                
                self.client.ping()
                self.connected = True
                print("Redis connected successfully")
                return
                
            except (redis.ConnectionError, redis.RedisError, Exception) as e:
                if attempt < self.max_retries - 1:
                    delay = self.base_delay * (2 ** attempt)  # Exponential backoff
                    time.sleep(delay)
                else:
                    if not self.warning_printed:
                        print(f"WARNING: Redis not available after {self.max_retries} attempts, using fallback mode: {str(e)}")
                        self.warning_printed = True
                    self.connected = False
    
    def is_connected(self) -> bool:
        """Check if Redis is connected."""
        return self.connected
    
    def log_entry(self, entry: dict) -> bool:
        """Store log entry in Redis (last 100 entries only)."""
        if not self.connected:
            return False
        try:
            log_data = json.dumps({
                **entry,
                "timestamp": time.time()
            })
            self.client.lpush("app_logs", log_data)
            self.client.ltrim("app_logs", 0, 99)  # Keep only last 100 items
            return True
        except Exception:
            # Silently fail - don't let logging crash the app
            return False
    
    def get_recent_logs(self, count: int = 100) -> list:
        """Get recent log entries from Redis."""
        if not self.connected:
            return []
        try:
            logs = self.client.lrange("app_logs", 0, count - 1)
            return [json.loads(log) for log in logs]
        except Exception:
            return []
    
    def health_check(self) -> dict:
        """Return Redis health status."""
        if not self.connected:
            return {
                "connected": False,
                "status": "disconnected",
                "error": "Redis connection not available"
            }
        
        try:
            self.client.ping()
            return {
                "connected": True,
                "status": "healthy",
                "url": self.redis_url.replace(self.redis_url.split('@')[0].split('//')[1], '***') if '@' in self.redis_url else self.redis_url
            }
        except Exception as e:
            self.connected = False
            return {
                "connected": False,
                "status": "error",
                "error": str(e)
            }

redis_client = RedisClient()