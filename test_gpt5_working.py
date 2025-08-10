import os
import sys
from openai import OpenAI
from dotenv import load_dotenv

# Set UTF-8 encoding for Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Load environment variables
load_dotenv('backend/.env')

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

print("Testing GPT-5 Models...")
print("-" * 50)

# GPT-5 models found
gpt5_models = [
    "gpt-5",
    "gpt-5-nano", 
    "gpt-5-mini",
    "gpt-5-chat-latest"
]

for model_name in gpt5_models:
    print(f"\nTesting {model_name}...")
    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Hello! What model are you and what are your capabilities?"}
            ],
            max_completion_tokens=100,  # Using max_completion_tokens instead of max_tokens
            temperature=0.7
        )
        
        print(f"✅ SUCCESS with {model_name}!")
        print(f"Response: {response.choices[0].message.content[:200]}...")
        print(f"Model used: {response.model}")
        print(f"Usage: {response.usage}")
        
        # Test for product listing generation
        print(f"\nTesting {model_name} for product listing generation...")
        listing_response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": "You are an expert e-commerce listing creator."},
                {"role": "user", "content": "Create a short product title for a wireless bluetooth headphone"}
            ],
            max_completion_tokens=50,
            temperature=0.7
        )
        print(f"Listing test: {listing_response.choices[0].message.content}")
        break  # Use the first working model
        
    except Exception as e:
        print(f"❌ Failed with {model_name}: {str(e)[:100]}")

print("\n" + "="*50)
print("Recommendation: Use 'gpt-5' or 'gpt-5-chat-latest' for best performance in your application!")