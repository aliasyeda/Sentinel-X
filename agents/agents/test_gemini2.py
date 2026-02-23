"""
Test Gemini with NEW library (google-genai)
"""
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    print("❌ ERROR: No API key found in .env file!")
    print("📋 Check your .env file:")
    try:
        with open('../.env', 'r') as f:
            print(f.read())
    except:
        print("No .env file found!")
    exit()

print(f"✅ API Key found: {api_key[:15]}...")

# Try NEW Google GenAI
try:
    import google.genai as genai
    print("✅ Using NEW google.genai library")
    
    client = genai.Client(api_key=api_key)
    
    # List available models
    print("\n📋 Available models:")
    models = client.models.list()
    for model in models:
        print(f"  - {model.name}")
    
    # Test with Gemini 2.0 Flash
    print("\n🧪 Testing Gemini 2.0 Flash...")
    response = client.models.generate_content(
        model="gemini-2.0-flash-exp",
        contents="Say 'Sentinel-X Prime is working with Gemini 2.0!'"
    )
    print(f"✅ Response: {response.text}")
    
except ImportError:
    print("❌ google.genai not installed")
    print("Install: pip install google-genai")
except Exception as e:
    print(f"❌ Error with new library: {e}")
    
    # Try OLD library as backup
    print("\n🔄 Trying OLD library...")
    try:
        import google.generativeai as old_genai
        old_genai.configure(api_key=api_key)
        
        # List OLD models
        print("OLD library models:")
        for model in old_genai.list_models():
            if 'generateContent' in model.supported_generation_methods:
                print(f"  - {model.name.split('/')[-1]}")
        
        # Test
        model = old_genai.GenerativeModel('gemini-1.5-pro')
        response = model.generate_content("Test")
        print(f"✅ OLD library works: {response.text[:50]}...")
        
    except Exception as e2:
        print(f"❌ Both libraries failed: {e2}")

