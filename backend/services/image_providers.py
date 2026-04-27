"""
Alternative image generation providers
Since Gemini doesn't support image generation yet, we provide multiple options
"""

import os
import requests
from typing import List

# Option 1: Keep OpenAI for images only
def generate_with_openai(prompt: str, count: int = 2) -> List[str]:
    """Use OpenAI DALL-E for image generation"""
    try:
        from openai import OpenAI
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        image_urls = []
        for _ in range(count):
            response = client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1024",
                quality="standard",
                n=1
            )
            image_urls.append(response.data[0].url)
        
        return image_urls
    except Exception as e:
        print(f"OpenAI image generation error: {e}")
        return []

# Option 2: Stability AI (Stable Diffusion)
def generate_with_stability(prompt: str, count: int = 2) -> List[str]:
    """
    Use Stability AI for image generation
    Requires STABILITY_API_KEY in .env
    """
    api_key = os.getenv("STABILITY_API_KEY")
    if not api_key:
        print("STABILITY_API_KEY not found")
        return []
    
    try:
        url = "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image"
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        
        image_urls = []
        for _ in range(count):
            body = {
                "text_prompts": [{"text": prompt}],
                "cfg_scale": 7,
                "height": 1024,
                "width": 1024,
                "samples": 1,
                "steps": 30,
            }
            
            response = requests.post(url, headers=headers, json=body)
            
            if response.status_code == 200:
                data = response.json()
                # Stability returns base64 images, you'd need to save/host them
                # For simplicity, returning empty for now
                print("Stability AI generation successful")
            else:
                print(f"Stability AI error: {response.status_code}")
        
        return image_urls
    except Exception as e:
        print(f"Stability AI error: {e}")
        return []

# Option 3: Placeholder for Google Vertex AI Imagen
def generate_with_imagen(prompt: str, count: int = 2) -> List[str]:
    """
    Use Google Vertex AI Imagen
    Requires Google Cloud setup and credentials
    """
    print("⚠️ Vertex AI Imagen requires Google Cloud setup")
    print("Visit: https://cloud.google.com/vertex-ai/docs/generative-ai/image/overview")
    return []

# Recommended approach: Use OpenAI for images, Gemini for text
ACTIVE_IMAGE_PROVIDER = generate_with_openai

def generate_images(prompt: str, count: int = 2) -> List[str]:
    """
    Main image generation function
    Uses the active provider (currently OpenAI)
    """
    return ACTIVE_IMAGE_PROVIDER(prompt, count)