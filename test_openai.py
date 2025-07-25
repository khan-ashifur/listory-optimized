#!/usr/bin/env python
"""
Test OpenAI client directly
"""
import os
from openai import OpenAI

# Load API key from .env file in backend directory
import os

def load_env_key():
    env_file = os.path.join(os.path.dirname(__file__), 'backend', '.env')
    print(f"Looking for .env file at: {env_file}")
    
    if os.path.exists(env_file):
        print("✅ Found .env file")
        with open(env_file, 'r') as f:
            lines = f.readlines()
            for line in lines:
                if line.startswith('OPENAI_API_KEY='):
                    key = line.split('=', 1)[1].strip()
                    return key
    else:
        print("❌ .env file not found")
    
    return ''

api_key = load_env_key()

print("🔍 Testing OpenAI Client...")
print("=" * 40)

print(f"API Key: {api_key[:10]}..." if api_key else "No API Key found")

if not api_key or api_key == 'your-openai-api-key-here':
    print("❌ OpenAI API key not configured")
    exit(1)

try:
    print("\n1️⃣  Testing OpenAI client initialization...")
    client = OpenAI(api_key=api_key)
    print("✅ Client initialized successfully")
    
    print("\n2️⃣  Testing API call...")
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # Use cheaper model for testing
        messages=[{"role": "user", "content": "Say 'Hello World'"}],
        max_tokens=10
    )
    
    result = response.choices[0].message.content
    print(f"✅ API call successful: {result}")
    
except Exception as e:
    print(f"❌ Error: {e}")
    
    # Try alternative initialization
    try:
        print("\n🔄 Trying legacy method...")
        import openai
        openai.api_key = api_key
        
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "Say 'Hello World'"}],
            max_tokens=10
        )
        
        result = response.choices[0].message.content
        print(f"✅ Legacy method successful: {result}")
        
    except Exception as e2:
        print(f"❌ Legacy method also failed: {e2}")

print("\n" + "=" * 40)
print("🔍 OpenAI test completed!")