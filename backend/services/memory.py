from typing import List, Dict

class ConversationMemory:
    """
    Simple in-memory conversation storage
    In production, use Redis or database
    """
    def __init__(self, max_history: int = 5):
        self.conversations: Dict[str, List[dict]] = {}
        self.max_history = max_history
    
    def add_message(self, session_id: str, role: str, content: str):
        """Add a message to conversation history"""
        if session_id not in self.conversations:
            self.conversations[session_id] = []
        
        self.conversations[session_id].append({
            "role": role,
            "content": content
        })
        
        # Keep only last N messages
        if len(self.conversations[session_id]) > self.max_history * 2:
            self.conversations[session_id] = self.conversations[session_id][-self.max_history * 2:]
    
    def get_history(self, session_id: str) -> List[dict]:
        """Get conversation history for a session"""
        return self.conversations.get(session_id, [])
    
    def clear_history(self, session_id: str):
        """Clear conversation history"""
        if session_id in self.conversations:
            del self.conversations[session_id]

# Global memory instance
memory = ConversationMemory()