from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from models.schemas import ChatRequest, ChatResponse
from services.intent import detect_intent
from services.enhancer import enhance_prompt
from services.generator import generate_images, generate_text, generate_hybrid
from services.memory import memory
import uuid
import requests
import time
import traceback

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Main chat endpoint with proper error handling
    """
    try:
        user_message = request.message
        history = request.history or []
        
        print(f"\n{'='*60}")
        print(f"📨 New chat request")
        print(f"{'='*60}")
        print(f"👤 User message: {user_message}")
        print(f"📋 History items: {len(history)}")
        
        # Validate input
        if not user_message or not user_message.strip():
            raise HTTPException(status_code=400, detail="Message cannot be empty")
        
        session_id = "default_session"
        
        # Step 1: Detect intent
        print(f"\n🔍 Step 1: Detecting intent...")
        intent = detect_intent(user_message)
        print(f"✅ Intent detected: {intent}")
        
        # Step 2: Enhance prompt
        print(f"\n✨ Step 2: Enhancing prompt...")
        enhanced_prompt = enhance_prompt(user_message, intent)
        print(f"✅ Enhanced prompt: {enhanced_prompt[:80]}...")
        
        # Step 3: Generate content based on intent
        print(f"\n🎨 Step 3: Generating {intent} content...")
        
        if intent == "image":
            # Generate images
            print(f"   Generating images...")
            image_urls = generate_images(enhanced_prompt, count=2)
            
            if not image_urls:
                raise Exception("No images were generated")
            
            print(f"✅ Generated {len(image_urls)} images")
            
            # Store in memory
            memory.add_message(session_id, "user", user_message)
            memory.add_message(session_id, "assistant", f"Generated {len(image_urls)} images")
            
            return ChatResponse(
                type="images",
                data=image_urls,
                metadata={
                    "enhanced_prompt": enhanced_prompt,
                    "intent": intent
                }
            )
        
        elif intent == "text":
            # Generate text
            print(f"   Generating text...")
            text_content = generate_text(enhanced_prompt, history)
            
            if not text_content:
                raise Exception("No text was generated")
            
            print(f"✅ Text generated ({len(text_content)} characters)")
            
            # Store in memory
            memory.add_message(session_id, "user", user_message)
            memory.add_message(session_id, "assistant", text_content)
            
            return ChatResponse(
                type="text",
                data=text_content,
                metadata={
                    "enhanced_prompt": enhanced_prompt,
                    "intent": intent
                }
            )
        
        elif intent == "hybrid":
            # Generate both text and images
            print(f"   Generating text and images...")
            hybrid_content = generate_hybrid(enhanced_prompt, history)
            
            if not hybrid_content.get("text"):
                raise Exception("Failed to generate hybrid text content")
            
            if not hybrid_content.get("images") or len(hybrid_content.get("images", [])) == 0:
                raise Exception("Failed to generate hybrid images")
            
            print(f"✅ Hybrid content generated")
            print(f"   Text: {len(hybrid_content['text'])} characters")
            print(f"   Images: {len(hybrid_content['images'])} images")
            
            # Store in memory
            memory.add_message(session_id, "user", user_message)
            memory.add_message(session_id, "assistant", hybrid_content["text"])
            
            # Return hybrid response with proper structure
            return ChatResponse(
                type="hybrid",
                data={
                    "text": hybrid_content["text"],
                    "images": hybrid_content["images"]
                },
                metadata={
                    "enhanced_prompt": enhanced_prompt,
                    "intent": intent
                }
            )
        
        else:
            raise HTTPException(status_code=400, detail=f"Unknown intent type: {intent}")
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"\n❌ Chat error: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "Vizzy Chat API"}

@router.get("/image-proxy")
async def proxy_image(url: str):
    """
    Proxy image requests to bypass CORS issues
    With retry logic for timeouts
    """
    try:
        if not url:
            raise HTTPException(status_code=400, detail="URL parameter required")
        
        print(f"📥 Proxying image: {url[:80]}...")
        
        max_retries = 3
        timeout = 120
        
        for attempt in range(max_retries):
            try:
                print(f"   Attempt {attempt + 1}/{max_retries}...")
                
                response = requests.get(url, timeout=timeout)
                
                if response.status_code == 200:
                    print(f"✅ Image proxied successfully (attempt {attempt + 1})")
                    
                    return StreamingResponse(
                        iter([response.content]),
                        media_type="image/png",
                        headers={
                            "Cache-Control": "max-age=3600",
                            "Access-Control-Allow-Origin": "*",
                            "Content-Length": str(len(response.content))
                        }
                    )
                else:
                    print(f"⚠️ Status {response.status_code}, retrying...")
                    if attempt < max_retries - 1:
                        time.sleep(2)
                    continue
                    
            except requests.exceptions.Timeout:
                print(f"⏱️ Timeout on attempt {attempt + 1}/{max_retries}")
                
                if attempt < max_retries - 1:
                    print(f"   Retrying...")
                    time.sleep(3)
                    continue
                else:
                    print(f"❌ All retries exhausted")
                    raise HTTPException(status_code=504, detail="Image generation timeout")
                    
            except Exception as e:
                print(f"❌ Error on attempt {attempt + 1}: {e}")
                
                if attempt < max_retries - 1:
                    time.sleep(2)
                    continue
                else:
                    raise
        
        raise HTTPException(status_code=504, detail="Failed to fetch image after retries")
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Proxy error: {e}")
        raise HTTPException(status_code=500, detail=str(e))