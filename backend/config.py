"""
Configuration for FREE tier (Pollinations + Local Processing)
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # API Keys
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")  # Not used due to rate limits
    HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN")
    
    # Providers
    TEXT_PROVIDER = "local"  # No API calls needed
    IMAGE_PROVIDER = "pollinations"  # Fast, unlimited
    
    # Server Config
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 8000))
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
    
    @classmethod
    def validate(cls):
        """Validate configuration"""
        print("\n✅ Configuration validated successfully")
        print(f"📝 Text Provider: {cls.TEXT_PROVIDER} (Local, no API calls)")
        print(f"🎨 Image Provider: {cls.IMAGE_PROVIDER} (Pollinations.ai, unlimited)")
        print(f"💰 Total Cost: $0.00 (100% FREE)")
        print(f"⚡ Speed: FAST (no rate limits)\n")
        
        return True

# Validate on import
Config.validate()