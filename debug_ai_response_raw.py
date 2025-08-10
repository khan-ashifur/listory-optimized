"""
Debug Raw AI Response for German Characters
Check if German characters are present in the original AI response
"""

import os
import sys
import django

# Add the backend directory to the Python path
sys.path.insert(0, r'C:\Users\khana\Desktop\listory-ai\backend')

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "listory.settings")
django.setup()

from apps.core.models import Product
from apps.listings.services import ListingGeneratorService
from openai import OpenAI
from django.conf import settings

def test_raw_ai_response():
    """Generate a German listing and examine the raw response"""
    print("🔍 TESTING RAW AI RESPONSE FOR GERMAN CHARACTERS")
    print("="*60)
    
    try:
        # Get OpenAI client
        if not settings.OPENAI_API_KEY or not settings.OPENAI_API_KEY.startswith('sk-'):
            print("❌ OpenAI API key not configured")
            return
            
        client = OpenAI(api_key=settings.OPENAI_API_KEY)
        
        # Create a simple German prompt
        prompt = """
🚨🚨🚨 CRITICAL LANGUAGE REQUIREMENT 🚨🚨🚨
YOU MUST WRITE EVERYTHING IN GERMAN!
NOT A SINGLE WORD IN ENGLISH!

LANGUAGE: German for Deutschland
TARGET MARKET: Amazon.de

ALL CONTENT MUST BE IN GERMAN:
- Title: COMPLETELY in German
- Bullet Points: COMPLETELY in German  
- Description: COMPLETELY in German

Create a German Amazon listing for a handheld misting fan. Use proper German with ä, ö, ü, ß characters.

Include words like:
- für (for)
- größe (size) 
- heiß (hot)
- kühlen (cool)
- natürlich (natural)
- tragbarer (portable)

Return ONLY valid JSON:

{
  "productTitle": "German title with German characters",
  "bulletPoints": [
    "German bullet with ä, ö, ü, ß characters",
    "Another German bullet point"
  ],
  "productDescription": "German description with proper characters"
}
"""
        
        print("📤 Sending prompt to OpenAI...")
        print(f"Prompt includes test words: für, größe, heiß, kühlen")
        
        # Make API call
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2000,
            temperature=0.7
        )
        
        raw_content = response.choices[0].message.content
        
        print(f"📥 Raw AI Response received: {len(raw_content)} characters")
        print(f"\n🔤 RAW RESPONSE PREVIEW:")
        print("="*50)
        print(raw_content[:500])
        print("="*50)
        
        # Analyze German characters in raw response
        german_chars = ['ä', 'ö', 'ü', 'ß', 'Ä', 'Ö', 'Ü']
        found_chars = {}
        for char in german_chars:
            count = raw_content.count(char)
            if count > 0:
                found_chars[char] = count
                
        print(f"\n🇩🇪 GERMAN CHARACTER ANALYSIS:")
        if found_chars:
            print("✅ German characters found in raw response:")
            for char, count in found_chars.items():
                print(f"   {char}: {count} times")
        else:
            print("❌ No German characters found in raw response")
            
        # Check for German words
        german_test_words = ['für', 'größe', 'heiß', 'kühlen', 'natürlich', 'tragbarer']
        found_words = [word for word in german_test_words if word in raw_content]
        print(f"\n🔤 GERMAN WORD ANALYSIS:")
        if found_words:
            print("✅ German test words found:")
            for word in found_words:
                print(f"   {word}")
        else:
            print("❌ No German test words found")
            
        # Check all Unicode characters
        unicode_chars = set()
        for char in raw_content:
            if ord(char) > 127:
                unicode_chars.add((char, ord(char)))
                
        print(f"\n🌐 UNICODE CHARACTER ANALYSIS:")
        if unicode_chars:
            print("✅ Unicode characters found:")
            for char, code in sorted(list(unicode_chars)[:20]):  # Show first 20
                print(f"   {char} (U+{code:04X})")
        else:
            print("❌ No Unicode characters found")
            
        # Test JSON parsing
        try:
            import json
            parsed = json.loads(raw_content)
            print(f"\n✅ JSON parsing successful")
            
            if 'productTitle' in parsed:
                title = parsed['productTitle']
                title_german_chars = [char for char in german_chars if char in title]
                print(f"   Title German chars: {title_german_chars}")
                print(f"   Title: {title}")
                
        except Exception as e:
            print(f"\n❌ JSON parsing failed: {e}")
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_raw_ai_response()