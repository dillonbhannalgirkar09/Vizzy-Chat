"""
Free image generation using Pollinations.ai
"""
import requests
import os
import time
from typing import List
import urllib.parse

class FreeImageGenerator:
    """
    Generate images using FREE Pollinations.ai
    Returns direct image URLs
    """
    
    def __init__(self):
        self.api_token = os.getenv("HUGGINGFACE_TOKEN")
        print("✅ Using Pollinations.ai for image generation")
    
    def clean_prompt(self, prompt: str) -> str:
        """
        Clean prompt by removing quotes and extra characters
        """
        # Remove quotes and commas (they cause issues)
        clean = prompt.replace('"', '').replace("'", '')
        # Keep only alphanumeric, spaces, and basic punctuation
        clean = ''.join(c for c in clean if c.isalnum() or c in ' -_')
        # Remove extra spaces
        clean = ' '.join(clean.split())
        return clean
    
    def generate_with_pollinations(self, prompt: str, num_images: int = 2) -> List[str]:
        """
        Generate images using Pollinations.ai
        Returns direct image URLs (optimized for speed)
        """
        images = []
        
        # Clean the prompt
        clean_prompt = self.clean_prompt(prompt)
        print(f"🎨 Generating {num_images} images...")
        print(f"📝 Cleaned prompt: {clean_prompt}")
        
        for i in range(num_images):
            try:
                # Create unique seed for variation
                seed = i * 12345
                
                # Properly encode the prompt
                encoded_prompt = urllib.parse.quote(clean_prompt)
                
                # Pollinations.ai endpoint - optimized parameters
                # Using simpler/faster model settings
                image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=768&height=768&seed={seed}&nologo=true"
                
                print(f"✅ Image {i+1} URL generated")
                print(f"   Seed: {seed}")
                
                images.append(image_url)
                
                # Minimal delay between URL generation
                if i < num_images - 1:
                    time.sleep(0.5)
                
            except Exception as e:
                print(f"❌ Error generating image {i+1}: {e}")
        
        print(f"✅ Generated {len(images)} image URLs")
        return images
    
    def generate_images(self, prompt: str, num_images: int = 2) -> List[str]:
        """
        Main entry point
        Returns list of image URLs
        """
        return self.generate_with_pollinations(prompt, num_images)

# Global instance
free_generator = FreeImageGenerator()