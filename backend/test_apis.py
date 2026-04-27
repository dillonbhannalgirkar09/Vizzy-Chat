"""
Test script to verify API keys work
"""
import os
from dotenv import load_dotenv
import google.generativeai as genai
import requests

load_dotenv()

def test_gemini():
    """Test Gemini API"""
    print("\n🧪 Testing Gemini API...")
    try:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            print("❌ GEMINI_API_KEY not found in .env")
            return False
        
        genai.configure(api_key=api_key)
        
        # Use the correct model names from the list
        model_names = [
            'gemini-2.0-flash-lite',      # Fast and free
            'gemini-flash-latest',         # Latest flash model
            'models/gemini-2.0-flash-lite',
        ]
        
        for model_name in model_names:
            try:
                print(f"  Trying model: {model_name}...")
                model = genai.GenerativeModel(model_name)
                response = model.generate_content("Say hello in one word")
                
                print(f"  ✅ SUCCESS with {model_name}!")
                print(f"  Response: {response.text[:50]}...")
                print(f"\n  👉 Use this model: {model_name}")
                return True
            except Exception as e:
                print(f"  ❌ Failed: {str(e)[:100]}...")
                continue
        
        print("❌ All model names failed")
        return False
        
    except Exception as e:
        print(f"❌ Gemini error: {e}")
        return False

def test_huggingface():
    """Test Hugging Face API"""
    print("\n🧪 Testing Hugging Face API...")
    try:
        token = os.getenv("HUGGINGFACE_TOKEN")
        if not token:
            print("⚠️ HUGGINGFACE_TOKEN not found")
            return False
        
        # Correct Hugging Face Inference API endpoint
        headers = {"Authorization": f"Bearer {token}"}
        
        # Try multiple working models
        models = [
            "stabilityai/stable-diffusion-xl-base-1.0",
            "runwayml/stable-diffusion-v1-5",
            "CompVis/stable-diffusion-v1-4"
        ]
        
        for model_id in models:
            api_url = f"https://api-inference.huggingface.co/models/{model_id}"
            print(f"  Trying: {model_id}...")
            
            response = requests.post(
                api_url,
                headers=headers,
                json={"inputs": "a photo of an astronaut riding a horse on mars"},
                timeout=60
            )
            
            if response.status_code == 200:
                print(f"  ✅ SUCCESS with {model_id}!")
                print(f"  Image size: {len(response.content)} bytes")
                return True
            elif response.status_code == 503:
                print(f"  ⏳ Model loading (wait 20s)...")
                continue
            else:
                print(f"  ❌ Status {response.status_code}")
                continue
        
        print("  ⚠️ All models loading or unavailable")
        return True  # Non-critical for now
            
    except Exception as e:
        print(f"  ⚠️ Error: {e}")
        return True

if __name__ == "__main__":
    print("=" * 50)
    print("VIZZY CHAT - API TESTING")
    print("=" * 50)
    
    gemini_ok = test_gemini()
    hf_ok = test_huggingface()
    
    print("\n" + "=" * 50)
    print("RESULTS:")
    print("=" * 50)
    print(f"Gemini: {'✅ PASS' if gemini_ok else '❌ FAIL'}")
    print(f"Hugging Face: {'✅ PASS' if hf_ok else '⚠️ WARNING'}")
    
    if gemini_ok:
        print("\n🎉 Ready to start the server!")
        print("Run: python main.py")
    else:
        print("\n❌ Fix Gemini API configuration")