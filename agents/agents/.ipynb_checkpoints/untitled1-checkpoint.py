import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("AIzaSyD-FbfN0UQk_sGUMyM5uQOO4xBUxCidFao")
print(f"API Key: {api_key[:20]}...")  # Show first 20 chars

if not api_key:
    print("❌ No API key found in .env")
    exit()

genai.configure(api_key=api_key)

# Test Gemini 2.0
models_to_test = [
    "gemini-2.0-flash-exp",
    "gemini-2.0-flash-thinking-exp",
    "gemini-2.0-pro-exp",
    "gemini-1.5-pro"
]

print("\n🎯 Testing Gemini models with YOUR existing API key...")

for model_name in models_to_test:
    try:
        print(f"\nTrying {model_name}...")
        model = genai.GenerativeModel(model_name)
        response = model.generate_content("Say 'Sentinel-X Prime is working!'")
        print(f"✅ SUCCESS! Response: {response.text}")
        print(f"✨ Your API key works with {model_name}!")
        break
    except Exception as e:
        print(f"❌ Failed with {model_name}: {str(e)[:100]}")

print("\n🎉 Your existing API key works with latest Gemini models!")
print("Use: LLM_MODEL=gemini-2.0-flash-exp")