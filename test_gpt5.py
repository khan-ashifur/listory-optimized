import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv('backend/.env')

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

print("Checking available OpenAI models...")
print("-" * 50)

try:
    # List all available models
    models = client.models.list()
    
    # Filter and display GPT models
    gpt_models = []
    for model in models.data:
        if 'gpt' in model.id.lower():
            gpt_models.append(model.id)
            print(f"Found: {model.id}")
    
    print("-" * 50)
    
    # Check specifically for GPT-5
    gpt5_models = [m for m in gpt_models if 'gpt-5' in m.lower() or 'gpt5' in m.lower()]
    
    if gpt5_models:
        print(f"\n✅ GPT-5 FOUND! Models: {gpt5_models}")
        
        # Test GPT-5
        print("\nTesting GPT-5 API...")
        test_model = gpt5_models[0]
        
        response = client.chat.completions.create(
            model=test_model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Hello! What model are you? Please confirm if you are GPT-5."}
            ],
            max_tokens=100,
            temperature=0.7
        )
        
        print(f"\nGPT-5 Response: {response.choices[0].message.content}")
        print(f"\n✅ GPT-5 API test successful! Model '{test_model}' is working.")
        
    else:
        print("\n❌ GPT-5 not found in available models.")
        
        # Test with latest available GPT-4 model
        print("\nAvailable GPT-4 models:")
        gpt4_models = [m for m in gpt_models if 'gpt-4' in m.lower()]
        for model in gpt4_models[:5]:  # Show first 5 GPT-4 models
            print(f"  - {model}")
        
        # Try GPT-4 Turbo or latest
        test_models = ['gpt-4-turbo', 'gpt-4-turbo-preview', 'gpt-4-1106-preview', 'gpt-4']
        
        for test_model in test_models:
            try:
                print(f"\nTesting {test_model}...")
                response = client.chat.completions.create(
                    model=test_model,
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": "What model are you?"}
                    ],
                    max_tokens=50
                )
                print(f"✅ {test_model} is working!")
                print(f"Response: {response.choices[0].message.content}")
                break
            except Exception as e:
                print(f"❌ {test_model} failed: {str(e)[:100]}")
                
except Exception as e:
    print(f"Error checking models: {e}")
    
    # Try directly with GPT-5 in case it's not listed
    print("\nAttempting direct GPT-5 access...")
    try:
        response = client.chat.completions.create(
            model="gpt-5",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Hello! Are you GPT-5?"}
            ],
            max_tokens=50
        )
        print("✅ GPT-5 direct access successful!")
        print(f"Response: {response.choices[0].message.content}")
    except Exception as e2:
        print(f"❌ Direct GPT-5 access failed: {str(e2)[:200]}")