"""
Prompt enhancement - using simple strategies
Gemini free tier is rate limited, so we use fast enhancement without API calls
"""
import os

# Disabled: Gemini is rate limited on free tier
# import google.generativeai as genai
# genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def enhance_prompt(user_message: str, intent_type: str) -> str:
    """
    Enhance user prompt using simple strategies (NO API CALLS)
    """
    return enhance_prompt_local(user_message, intent_type)

def enhance_prompt_local(user_message: str, intent_type: str) -> str:
    """
    Fast local prompt enhancement without API calls
    """
    if intent_type == "image" or intent_type == "hybrid":
        return enhance_for_image(user_message)
    else:
        return enhance_for_text(user_message)

def enhance_for_image(prompt: str) -> str:
    """
    Enhance image generation prompts locally
    """
    # Add quality markers
    quality_markers = [
        "detailed",
        "professional",
        "high quality",
        "4k",
        "cinematic",
        "sharp focus",
        "trending on artstation"
    ]
    
    # Add artistic style if not present
    artistic_styles = [
        "beautifully composed",
        "well-lit",
        "vibrant colors"
    ]
    
    enhanced = prompt
    
    # Add quality if not already present
    if "4k" not in enhanced.lower() and "quality" not in enhanced.lower():
        enhanced += f", {quality_markers[0]}, {quality_markers[1]}"
    
    # Add artistic touch if short
    if len(enhanced) < 50:
        enhanced += f", {artistic_styles[0]}"
    
    print(f"✨ Enhanced prompt for image generation")
    return enhanced

def enhance_for_text(prompt: str) -> str:
    """
    Enhance text generation prompts locally
    """
    # Keep it simple for text
    # Add context if missing
    
    if len(prompt) < 20:
        enhanced = f"Create a detailed response to: {prompt}"
    else:
        enhanced = prompt
    
    print(f"✨ Enhanced prompt for text generation")
    return enhanced

# For backward compatibility
# def enhance_prompt_gemini(user_message: str, intent_type: str) -> str:
#     """
#     OLD: Gemini-based prompt enhancement
#     DISABLED due to rate limiting
#     """
#     pass