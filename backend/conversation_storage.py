from agents import SQLiteSession
from typing import Dict
import threading
import os

class ConversationManager:
    """Manages conversation sessions using OpenAI Agents SDK session management"""
    
    def __init__(self, db_path: str = "conversations.db"):
        self.db_path = db_path
        self._sessions: Dict[str, SQLiteSession] = {}
        self._lock = threading.Lock()
        
        # Ensure the database directory exists
        db_dir = os.path.dirname(db_path) if os.path.dirname(db_path) else "."
        os.makedirs(db_dir, exist_ok=True)
    
    def get_session(self, thread_id: str) -> SQLiteSession:
        """Get or create a session for a given thread_id"""
        with self._lock:
            if thread_id not in self._sessions:
                # Create a new session for this thread_id
                self._sessions[thread_id] = SQLiteSession(
                    session_id=thread_id,
                    db_path=self.db_path
                )
            return self._sessions[thread_id]
    
    async def clear_session(self, thread_id: str) -> None:
        """Clear a specific conversation session"""
        with self._lock:
            if thread_id in self._sessions:
                # Clear the session data
                session = self._sessions[thread_id]
                await session.clear_session()
                
                # Remove from our cache
                del self._sessions[thread_id]
    
    def close_session(self, thread_id: str) -> None:
        """Close and remove a session from the cache"""
        with self._lock:
            if thread_id in self._sessions:
                del self._sessions[thread_id]

# Global conversation manager instance
conversation_manager = ConversationManager() 