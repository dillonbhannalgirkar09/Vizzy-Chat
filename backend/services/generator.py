"""
Content generation using local methods + Pollinations
"""
import os
from typing import List, Dict
from services.free_image_generator import free_generator

def generate_images(prompt: str, count: int = 2) -> List[str]:
    """
    Generate images using Pollinations (FREE, unlimited)
    """
    try:
        print(f"🎨 Generating {count} images...")
        return free_generator.generate_images(prompt, num_images=count)
    except Exception as e:
        print(f"❌ Image generation error: {e}")
        return []

def generate_text(prompt: str, history: List[Dict] = None) -> str:
    """
    Generate text using a simple template-based approach
    Handles conversation history
    """
    try:
        print(f"📝 Generating text response...")
        print(f"   History length: {len(history) if history else 0}")
        
        # Simple creative response generation
        responses = {
            "story": generate_story(prompt),
            "poem": generate_poem(prompt),
            "description": generate_description(prompt),
            "default": generate_creative_response(prompt)
        }
        
        # Determine which type based on prompt
        prompt_lower = prompt.lower()
        
        if "story" in prompt_lower or "tale" in prompt_lower:
            return responses["story"]
        elif "poem" in prompt_lower:
            return responses["poem"]
        elif "describe" in prompt_lower or "tell" in prompt_lower:
            return responses["description"]
        else:
            return responses["default"]
    
    except Exception as e:
        print(f"❌ Text generation error: {e}")
        import traceback
        traceback.print_exc()
        return "I encountered an error generating content. Please try again."

def generate_story(prompt: str) -> str:
    """Generate a simple story"""
    return f"""✨ **A Creative Tale**

Once upon a time, {prompt.lower()}...

In a world full of possibilities, this moment unfolded beautifully. 
The details came together perfectly, creating something truly special.

Every element played its part, weaving together into a tapestry of wonder.
And so the story continued, bringing joy and inspiration to all who witnessed it.

*The End* 📖"""

def generate_poem(prompt: str) -> str:
    """Generate a simple poem"""
    words = prompt.split()[:5]  # Get first 5 words
    
    return f"""✨ **A Poetic Expression**

{' '.join(words)},
Dancing through the mind's eye,
Creating visions both bold and bright,
Where imagination takes flight.

In each moment, beauty shines,
A reflection of the soul's design,
Words and images intertwine,
Creating something truly divine.

Through colors, shapes, and heartfelt thoughts,
The world becomes what we have sought,
A canvas of our deepest dreams,
More beautiful than it seems.

*- Vizzy* 🎨"""

def generate_description(prompt: str) -> str:
    """Generate a descriptive response"""
    return f"""✨ **Description & Vision**

Imagine this: {prompt}

**Visual Elements:**
- Rich, vibrant colors that draw the eye
- Careful composition creating balance
- Details that tell a deeper story
- Atmosphere that evokes emotion

**Creative Interpretation:**
This concept brings together elements of beauty, imagination, and artistry. 
The interplay of light and shadow creates depth and dimension, 
while the overall composition guides the viewer's journey through the piece.

Every aspect has been thoughtfully considered to create 
a cohesive and inspiring visual narrative.

✨ *Brought to life by Vizzy* 🎨"""

def generate_creative_response(prompt: str) -> str:
    """Generate a general creative response"""
    return f"""✨ **Creative Response**

Thank you for your request: "{prompt}"

**What We're Creating:**
Your vision comes to life through a carefully crafted process:

1. **Ideation** - Understanding your creative intent
2. **Enhancement** - Adding artistic depth and sophistication  
3. **Visualization** - Bringing your imagination to visual form
4. **Refinement** - Polishing every detail to perfection

**The Result:**
Visual content that captures emotion, tells a story, and inspires the viewer.
Whether for personal enjoyment, creative projects, or professional use,
this creation is designed to resonate and delight.

Ready to explore more? Keep creating! 🎨✨"""

def generate_hybrid(prompt: str, history: List[Dict] = None) -> dict:
    """
    Generate both text and images
    """
    try:
        print("🔄 Generating hybrid content (text + images)...")
        
        # Generate text
        text_content = generate_text(prompt, history)
        
        # Create image prompt from the text request
        image_prompt = f"{prompt}. Cinematic, detailed, professional, artistic, inspiring"
        
        # Generate images
        images = generate_images(image_prompt, count=2)
        
        return {
            "text": text_content,
            "images": images
        }
    
    except Exception as e:
        print(f"❌ Hybrid generation error: {e}")
        import traceback
        traceback.print_exc()
        return {
            "text": "Error generating content.",
            "images": []
        }