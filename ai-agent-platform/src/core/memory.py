from langchain.memory import ConversationBufferMemory, ConversationSummaryMemory
from langchain.schema import BaseMemory
import json
import os
from typing import Dict, Any, List

class InMemoryStorage:
    """In-memory storage fallback when Redis is not available"""
    
    def __init__(self):
        self.storage = {}
    
    def setex(self, key: str, ttl: int, value: str):
        self.storage[key] = value
    
    def get(self, key: str):
        return self.storage.get(key)
    
    def delete(self, key: str):
        if key in self.storage:
            del self.storage[key]

class RedisMemory:
    """Redis-based conversation memory for agents with fallback"""
    
    def __init__(self):
        try:
            import redis
            self.redis_client = redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379"))
            # Test connection
            self.redis_client.ping()
        except:
            print("⚠️  Redis not available, using in-memory storage")
            self.redis_client = InMemoryStorage()
    
    def save_conversation(self, session_id: str, messages: list):
        """Save conversation to Redis or memory"""
        key = f"conversation:{session_id}"
        self.redis_client.setex(key, 3600, json.dumps(messages))
    
    def load_conversation(self, session_id: str) -> list:
        """Load conversation from Redis or memory"""
        key = f"conversation:{session_id}"
        data = self.redis_client.get(key)
        if data:
            return json.loads(data) if isinstance(data, str) else json.loads(data.decode())
        return []
    
    def clear_conversation(self, session_id: str):
        """Clear conversation from Redis or memory"""
        key = f"conversation:{session_id}"
        self.redis_client.delete(key)

class MemoryManager:
    """Memory management for different agent types"""
    
    def __init__(self):
        self.redis_memory = RedisMemory()
    
    def get_buffer_memory(self, session_id: str) -> ConversationBufferMemory:
        """Get buffer memory for assistive agents"""
        memory = ConversationBufferMemory(return_messages=True)
        # Load existing conversation
        messages = self.redis_memory.load_conversation(session_id)
        for msg in messages:
            memory.chat_memory.add_message(msg)
        return memory
    
    def get_summary_memory(self, session_id: str, llm) -> ConversationSummaryMemory:
        """Get summary memory for long conversations"""
        memory = ConversationSummaryMemory(llm=llm, return_messages=True)
        # Load existing conversation
        messages = self.redis_memory.load_conversation(session_id)
        for msg in messages:
            memory.chat_memory.add_message(msg)
        return memory
    
    def save_memory(self, session_id: str, memory: BaseMemory):
        """Save memory state to Redis or memory"""
        messages = memory.chat_memory.messages
        self.redis_memory.save_conversation(session_id, [msg.dict() for msg in messages])

# Global memory manager instance
memory_manager = MemoryManager()