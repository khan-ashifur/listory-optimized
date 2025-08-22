#!/usr/bin/env python3
"""
Debug script to investigate Etsy listing generation issues
"""

import os
import sys
import django
import json

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory.settings')
django.setup()

from django.contrib.auth.models import User
from apps.core.models import Product
from apps.listings.models import GeneratedListing
from apps.listings.services import ListingGeneratorService

def debug_etsy_generation():
    """Debug the Etsy generation process step by step"""
    print("🔍 DEBUGGING ETSY LISTING GENERATION")
    print("="*50)
    
    # Get a test product
    try:
        product = Product.objects.filter(name='Custom Wedding Ring Holder').first()
        if not product:
            print("❌ Test product not found")
            return
        
        print(f"✅ Found test product: {product.name}")
        print(f"   Brand Tone: {product.brand_tone}")
        print(f"   Marketplace: {product.marketplace}")
        print(f"   Occasion: {product.occasion}")
        
        # Initialize service
        service = ListingGeneratorService()
        print(f"✅ Service initialized")
        print(f"   OpenAI client: {service.client is not None}")
        
        if not service.client:
            print("❌ OpenAI client not available - check API key")
            return
            
        # Test the specific Etsy generation method
        print("\n🎯 Testing _generate_etsy_listing method...")
        
        # Create a new listing object
        listing = GeneratedListing.objects.create(
            product=product,
            platform='etsy',
            status='processing'
        )
        
        print(f"✅ Created listing object: {listing.id}")
        
        # Get marketplace and occasion context
        marketplace_info = service._get_marketplace_context(product.marketplace)
        occasion_context = service._get_occasion_context(product.occasion) if product.occasion else ""
        
        print(f"✅ Marketplace info: {marketplace_info}")
        print(f"✅ Occasion context length: {len(occasion_context)}")
        
        # Build the exact prompt being sent
        prompt = f"""🎨 You are the WORLD'S BEST Etsy listing optimization expert, specializing in handmade, vintage, and creative items. Your listings consistently outperform Helium 10, Jasper AI, and CopyMonkey by focusing on emotional storytelling, authentic craftsmanship, and superior SEO optimization.

🌟 PRODUCT INFORMATION:
- Product Name: {product.name}
- Brand: {product.brand_name}
- Description: {product.description}
- Brand Tone: {product.brand_tone}
- Features: {product.features}
- Price: ${product.price}
- Categories: {product.categories}
- Target Keywords: {product.target_keywords or 'Generate automatically based on product'}
- Marketplace: {marketplace_info['country']} ({marketplace_info['language']})
- Brand Persona: {product.brand_persona or 'Authentic artisan focused on quality and uniqueness'}
- Target Audience: {product.target_audience or 'Creative individuals who value handmade quality and unique designs'}
{occasion_context}

🎯 ETSY SUCCESS REQUIREMENTS (SUPERIOR TO COMPETITORS):

📝 TITLE OPTIMIZATION (140 chars max, first 50-60 chars critical):
- Front-load with highest-traffic keywords
- Include brand tone keywords ({product.brand_tone})
- Natural keyword integration (no keyword stuffing)
- Appeal to gift-givers and collectors
- Include occasion keywords if relevant

🏷️ TAGS STRATEGY (Exactly 13 tags, 20 chars each):
- Mix high-traffic broad terms with long-tail specifics
- Include brand tone tags, occasion tags, style tags
- Target gift-giving scenarios
- Use buyer intent keywords (e.g., "gift for her", "wedding decor")
- Include material and technique tags

📖 DESCRIPTION STORYTELLING (First 160 chars for Google SEO):
- Hook: Emotional connection in first line
- Story: Creation process and inspiration
- Benefits: Why this item is special
- Materials: Detailed composition
- Care: Maintenance instructions
- Gift appeal: Why it makes perfect gifts
- Processing time and shipping info

🎨 BRAND TONE INTEGRATION:
{service._get_etsy_brand_tone_guidance(product.brand_tone)}

{marketplace_info['cultural_context']}

Return ONLY valid JSON with comprehensive Etsy optimization:
{{
  "etsy_title": "SEO-optimized title (max 140 chars, front-loaded keywords)",
  "etsy_description": "Compelling description with storytelling, materials, care instructions (first 160 chars optimized for Google)",
  "etsy_tags": ["tag1", "tag2", "tag3", "tag4", "tag5", "tag6", "tag7", "tag8", "tag9", "tag10", "tag11", "tag12", "tag13"],
  "etsy_materials": "Detailed materials list (wood, metal, fabric, etc.)",
  "etsy_processing_time": "1-3 business days" or "1-2 weeks" or "Made to order",
  "etsy_personalization": "Personalization options available (if applicable)",
  "etsy_who_made": "i_did" or "collective" or "someone_else",
  "etsy_when_made": "made_to_order" or appropriate time period,
  "etsy_category_path": "Appropriate Etsy category hierarchy",
  "etsy_style_tags": "Style-specific keywords for better discovery",
  "etsy_seasonal_keywords": "Season/occasion specific keywords",
  "etsy_target_demographics": "Primary buyer personas and demographics",
  "etsy_gift_suggestions": "Gift occasions this item is perfect for",
  "etsy_care_instructions": "How to care for and maintain this item",
  "etsy_story_behind": "Personal story or inspiration behind the creation",
  "etsy_sustainability_info": "Eco-friendly aspects or sustainable practices",
  "quality_optimization": {{
    "emotional_appeal": "How this creates emotional connection",
    "uniqueness_factor": "What makes this different from mass-produced items",
    "gift_positioning": "Why this makes an exceptional gift",
    "search_optimization": "Primary SEO strategy for Etsy search"
  }}
}}"""
        
        print(f"\n📝 Prompt length: {len(prompt)} characters")
        print("\n🤖 Sending request to OpenAI...")
        
        # Make the OpenAI request
        try:
            response = service.client.chat.completions.create(
                model="gpt-5-chat-latest",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_completion_tokens=2500
            )
            
            print(f"✅ Received response from OpenAI")
            print(f"   Response type: {type(response)}")
            
            # Extract the content
            content = response.choices[0].message.content
            print(f"   Content length: {len(content)}")
            print(f"   Content preview (first 200 chars): {content[:200]}")
            print(f"   Content type: {type(content)}")
            
            # Try to parse as JSON with markdown cleanup
            print(f"\n🔍 Attempting JSON parsing...")
            try:
                # Extract JSON from potential markdown code blocks
                clean_content = content.strip()
                
                # Remove markdown code block formatting if present
                if clean_content.startswith('```json'):
                    clean_content = clean_content[7:]  # Remove ```json
                if clean_content.startswith('```'):
                    clean_content = clean_content[3:]   # Remove ```
                if clean_content.endswith('```'):
                    clean_content = clean_content[:-3]  # Remove trailing ```
                
                clean_content = clean_content.strip()
                print(f"   Cleaned content length: {len(clean_content)}")
                print(f"   Cleaned content preview: {clean_content[:200]}...")
                
                result = json.loads(clean_content)
                print(f"✅ JSON parsing successful!")
                print(f"   Keys in result: {list(result.keys())}")
                
                # Check required fields
                required_fields = ['etsy_title', 'etsy_description', 'etsy_tags']
                for field in required_fields:
                    if field in result:
                        print(f"   ✅ {field}: {len(str(result[field]))} chars")
                    else:
                        print(f"   ❌ {field}: MISSING")
                        
            except json.JSONDecodeError as e:
                print(f"❌ JSON parsing failed: {e}")
                print(f"   Raw content: {repr(content)}")
                
                # Check if content is empty or whitespace
                if not content or content.isspace():
                    print("   ⚠️ Content is empty or whitespace only")
                else:
                    print(f"   ⚠️ Content appears to be non-JSON text")
                    
        except Exception as e:
            print(f"❌ OpenAI request failed: {e}")
            import traceback
            traceback.print_exc()
        
        # Clean up
        listing.delete()
        print(f"\n✅ Cleanup completed")
        
    except Exception as e:
        print(f"❌ Debug failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_etsy_generation()