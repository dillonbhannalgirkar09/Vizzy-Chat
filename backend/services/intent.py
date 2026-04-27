"""
Intent detection - using fallback keyword matching
Gemini free tier is rate limited, so we use fast keyword detection
"""
import os

# Disabled: Gemini is rate limited on free tier
# import google.generativeai as genai
# genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def detect_intent(user_message: str) -> str:
    """
    Detect user intent using keyword matching (NO API CALLS)
    Returns: "image", "text", or "hybrid"
    """
    return fallback_intent_detection(user_message)

def fallback_intent_detection(user_message: str) -> str:
    """
    Fast intent detection using keyword matching
    No API calls, no rate limits!
    """
    message_lower = user_message.lower()
    
    # Image keywords
    image_keywords = [
        'paint', 'draw', 'create', 'design', 'visualize', 'generate', 
        'art', 'image', 'picture', 'photo', 'artwork', 'illustration',
        'sketch', 'render', 'visual', 'graphic', 'poster', 'wallpaper'
    ]
    
    # Text keywords
    text_keywords = [
        'write', 'story', 'poem', 'script', 'copy', 'compose', 
        'describe', 'explain', 'narrative', 'tale', 'article', 'essay',
        'quote', 'text', 'sentence', 'paragraph'
    ]
    
    # Hybrid keywords (both image and text)
    hybrid_keywords = [
        'and visualize', 'and illustrate', 'and show', 'and depict',
        'storyboard', 'both', 'with images', 'with visuals',
        'and create', 'story and image', 'with picture'
    ]
    
    # Check for hybrid first (most specific)
    for keyword in hybrid_keywords:
        if keyword in message_lower:
            print(f"Intent: HYBRID (matched: '{keyword}')")
            return "hybrid"
    
    # Check for image
    for keyword in image_keywords:
        if keyword in message_lower:
            print(f"Intent: IMAGE (matched: '{keyword}')")
            return "image"
    
    # Check for text
    for keyword in text_keywords:
        if keyword in message_lower:
            print(f"Intent: TEXT (matched: '{keyword}')")
            return "text"
    
    # Default to image for ambiguous cases
    print(f"Intent: IMAGE (default)")
    return "image"

# For backward compatibility
# def detect_intent_gemini(user_message: str) -> str:
#     """
#     OLD: Gemini-based intent detection
#     DISABLED due to rate limiting
#     """
#     pass