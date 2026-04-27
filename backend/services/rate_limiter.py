"""
Rate limiter for Gemini API to avoid quota issues
"""
import time
from datetime import datetime, timedelta
from typing import Dict

class RateLimiter:
    """
    Simple rate limiter to prevent hitting Gemini quota
    Free tier: 60 requests/minute, 1500 requests/day
    """
    
    def __init__(self, requests_per_minute: int = 15, requests_per_day: int = 100):
        self.requests_per_minute = requests_per_minute
        self.requests_per_day = requests_per_day
        
        self.minute_requests: Dict[int, int] = {}
        self.daily_requests = 0
        self.last_reset_day = datetime.now().date()
        self.request_times = []
    
    def is_allowed(self) -> tuple[bool, str]:
        """
        Check if request is allowed
        Returns: (allowed: bool, message: str)
        """
        now = datetime.now()
        current_minute = now.hour * 60 + now.minute
        
        # Reset daily counter
        if now.date() > self.last_reset_day:
            self.daily_requests = 0
            self.last_reset_day = now.date()
        
        # Check daily limit
        if self.daily_requests >= self.requests_per_day:
            return False, f"Daily limit reached ({self.daily_requests}/{self.requests_per_day})"
        
        # Check minute limit
        if current_minute not in self.minute_requests:
            self.minute_requests[current_minute] = 0
        
        if self.minute_requests[current_minute] >= self.requests_per_minute:
            return False, f"Minute limit reached ({self.minute_requests[current_minute]}/{self.requests_per_minute})"
        
        return True, "OK"
    
    def record_request(self):
        """Record a successful request"""
        now = datetime.now()
        current_minute = now.hour * 60 + now.minute
        
        if current_minute not in self.minute_requests:
            self.minute_requests[current_minute] = 0
        
        self.minute_requests[current_minute] += 1
        self.daily_requests += 1
        
        print(f"📊 Requests: {self.daily_requests}/{self.requests_per_day} today, {self.minute_requests[current_minute]}/{self.requests_per_minute} this minute")
    
    def get_status(self) -> Dict:
        """Get current rate limit status"""
        now = datetime.now()
        current_minute = now.hour * 60 + now.minute
        
        minute_count = self.minute_requests.get(current_minute, 0)
        
        return {
            "daily_requests": self.daily_requests,
            "daily_limit": self.requests_per_day,
            "minute_requests": minute_count,
            "minute_limit": self.requests_per_minute,
            "remaining_today": self.requests_per_day - self.daily_requests,
            "remaining_this_minute": self.requests_per_minute - minute_count
        }

# Global instance
rate_limiter = RateLimiter(requests_per_minute=15, requests_per_day=100)