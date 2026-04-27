from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import chat
from dotenv import load_dotenv
from config import Config

# Load environment variables
load_dotenv()

# Validate configuration
try:
    Config.validate()
except ValueError as e:
    print(f"❌ Configuration error: {e}")
    print("\nPlease check your .env file and ensure GEMINI_API_KEY is set.")
    exit(1)

# Initialize FastAPI app
app = FastAPI(
    title="Vizzy Chat API",
    description="Conversational AI for creative content generation (100% FREE - Gemini + Hugging Face)",
    version="2.0.0 (Free Tier)"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat.router, prefix="/api", tags=["chat"])

@app.get("/")
async def root():
    return {
        "message": "Vizzy Chat API - FREE Tier",
        "version": "2.0.0",
        "status": "running",
        "providers": {
            "text": f"{Config.TEXT_PROVIDER} (Google Gemini Flash)",
            "image": f"{Config.IMAGE_PROVIDER} (Hugging Face)"
        },
        "cost": "$0.00 per request",
        "docs": "/docs"
    }

@app.get("/api/providers")
async def get_providers():
    """Get current AI provider configuration"""
    return {
        "text_provider": Config.TEXT_PROVIDER,
        "image_provider": Config.IMAGE_PROVIDER,
        "gemini_configured": bool(Config.GEMINI_API_KEY),
        "huggingface_configured": bool(Config.HUGGINGFACE_TOKEN),
        "cost_per_request": "$0.00",
        "rate_limits": {
            "gemini": "15 requests/minute, 1500 requests/day",
            "huggingface": "~100 requests/hour with token"
        }
    }

@app.get("/api/status")
async def get_status():
    """Get current system status and rate limits"""
    from services.rate_limiter import rate_limiter
    from config import Config
    
    return {
        "status": "healthy",
        "text_provider": Config.TEXT_PROVIDER,
        "image_provider": Config.IMAGE_PROVIDER,
        "rate_limits": rate_limiter.get_status(),
        "cost": "$0.00"
    }

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host=Config.HOST,
        port=Config.PORT,
        reload=True
    )