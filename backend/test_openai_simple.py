#!/usr/bin/env python
"""
Simple OpenAI test in backend directory - Legacy API (v0.28)
"""
import os
import openai

print("🔍 Testing OpenAI Client...")
print("=" * 40)

# Read .env file directly
env_file = '.env'
api_key = ''

if os.path.exists(env_file):
    print(f"✅ Found .env file at: {os.path.abspath(env_file)}")
    with open(env_file, 'r') as f:
        for line in f:
            if line.startswith('OPENAI_API_KEY='):
                api_key = line.split('=', 1)[1].strip()
                break
else:
    print(f"❌ .env file not found at: {os.path.abspath(env_file)}")

print(f"API Key found: {'✅' if api_key else '❌'}")
if api_key:
    print(f"API Key preview: {api_key[:15]}...")

if not api_key or api_key == 'sk-your-actual-openai-api-key-here':
    print("❌ OpenAI API key not properly configured")
    print("Please edit the .env file and set your real OpenAI API key")
    exit(1)

# Test with OpenAI 0.28 (legacy API)
try:
    print("\n1️⃣  Testing OpenAI legacy API (v0.28)...")
    import openai
    
    # Set API key
    openai.api_key = api_key
    print("✅ API key set")
    
    print("\n2️⃣  Testing API call...")
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Say 'Hello from Listory! AI is working!'"}],
        max_tokens=30
    )
    
    result = response.choices[0].message.content
    print(f"✅ API call successful!")
    print(f"AI Response: '{result}'")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print("Make sure you have openai==0.28.1 installed")

print("\n" + "=" * 40)
print("🔍 OpenAI test completed!")