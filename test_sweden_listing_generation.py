#!/usr/bin/env python3
"""
Test script to generate a Sweden marketplace listing and analyze quality
"""

import os
import sys
import django
import json
from datetime import datetime

# Add the backend directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory.settings')
django.setup()

from apps.core.models import Product
from apps.listings.services import ListingGeneratorService

def create_test_product():
    """Create test product for Sweden marketplace"""
    
    # Delete existing test products to avoid conflicts
    Product.objects.filter(name__icontains="Professional Kitchen Knife Set").delete()
    
    # Create a dummy user if needed
    from django.contrib.auth.models import User
    user, created = User.objects.get_or_create(username='testuser', defaults={'email': 'test@example.com'})
    
    product_data = {
        'user': user,
        'name': 'Professional Kitchen Knife Set',
        'description': 'High-quality stainless steel kitchen knife set with ergonomic handles, perfect for professional and home cooking',
        'brand_name': 'ChefMaster',
        'brand_tone': 'professional',
        'target_platform': 'amazon',
        'price': 149.99,
        'categories': 'Kitchen, Knives, Cooking Tools',
        'features': 'High-carbon stainless steel blades, Ergonomic handles for comfortable grip, 8-piece complete knife set, Professional grade quality, Dishwasher safe, Includes wooden knife block',
        'target_keywords': 'kitchen knife set, professional knives, stainless steel knives, cooking knives, chef knife set',
        'brand_persona': 'Professional chef quality at home',
        'marketplace': 'se',  # Sweden marketplace
        'marketplace_language': 'sv',     # Swedish language
    }
    
    product = Product.objects.create(**product_data)
    print(f"✅ Created test product: {product.name} (ID: {product.id})")
    return product

def generate_listing(product):
    """Generate listing for the test product"""
    
    print(f"\n🔄 Generating listing for product ID: {product.id}")
    print(f"📍 Marketplace: {product.marketplace}")
    print(f"🗣️ Language: {product.marketplace_language}")
    
    try:
        service = ListingGeneratorService()
        result = service.generate_listing(product.id, 'amazon')
        
        if result.get('success'):
            return result.get('listing')
        else:
            print(f"❌ Failed to generate listing: {result.get('error')}")
            return None
            
    except Exception as e:
        print(f"❌ Exception during listing generation: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return None

def analyze_listing_quality(listing):
    """Analyze the quality of the generated listing"""
    
    analysis = {
        'overall_quality': 'Unknown',
        'issues': [],
        'successes': [],
        'keyword_analysis': {},
        'aplus_analysis': {},
        'language_analysis': {}
    }
    
    if not listing:
        analysis['issues'].append("No listing generated")
        analysis['overall_quality'] = 'Failed'
        return analysis
    
    print(f"\n📊 ANALYZING LISTING QUALITY")
    print("=" * 50)
    
    # Check basic structure
    required_fields = ['product_title', 'bullet_points', 'product_description', 'keywords']
    for field in required_fields:
        if field in listing and listing[field]:
            analysis['successes'].append(f"✅ {field} generated")
        else:
            analysis['issues'].append(f"❌ Missing or empty {field}")
    
    # Analyze title
    if 'product_title' in listing:
        title = listing['product_title']
        print(f"\n📝 TITLE ANALYSIS:")
        print(f"Title: {title}")
        print(f"Length: {len(title)} characters")
        
        # Check for Swedish language
        swedish_indicators = ['kök', 'kniv', 'set', 'professionell', 'kvalitet', 'rostfritt', 'stål']
        english_indicators = ['kitchen', 'knife', 'professional', 'quality', 'stainless', 'steel']
        
        swedish_found = [word for word in swedish_indicators if word.lower() in title.lower()]
        english_found = [word for word in english_indicators if word.lower() in title.lower()]
        
        if swedish_found:
            analysis['successes'].append(f"✅ Swedish words detected: {swedish_found}")
        if english_found:
            analysis['issues'].append(f"❌ English words detected: {english_found}")
        
        analysis['language_analysis']['title'] = {
            'content': title,
            'length': len(title),
            'swedish_words': swedish_found,
            'english_words': english_found
        }
    
    # Analyze bullet points
    if 'bullet_points' in listing:
        bullets = listing['bullet_points']
        print(f"\n🔸 BULLET POINTS ANALYSIS:")
        print(f"Number of bullets: {len(bullets) if isinstance(bullets, list) else 'Invalid format'}")
        
        if isinstance(bullets, list):
            for i, bullet in enumerate(bullets, 1):
                print(f"Bullet {i}: {bullet}")
                print(f"  Length: {len(bullet)} characters")
                
                # Check language
                if any(word in bullet.lower() for word in ['kitchen', 'knife', 'professional', 'quality']):
                    analysis['issues'].append(f"❌ English words in bullet {i}")
                if any(word in bullet.lower() for word in ['kök', 'kniv', 'professionell', 'kvalitet']):
                    analysis['successes'].append(f"✅ Swedish words in bullet {i}")
        
        analysis['language_analysis']['bullets'] = {
            'count': len(bullets) if isinstance(bullets, list) else 0,
            'content': bullets if isinstance(bullets, list) else []
        }
    
    # Analyze keywords
    if 'keywords' in listing:
        keywords = listing['keywords']
        print(f"\n🏷️ KEYWORDS ANALYSIS:")
        print(f"Number of keywords: {len(keywords) if isinstance(keywords, list) else 'Invalid format'}")
        
        if isinstance(keywords, list):
            for keyword in keywords[:10]:  # Show first 10
                print(f"  - {keyword}")
                
            # Check language distribution
            english_keywords = [k for k in keywords if any(word in k.lower() for word in ['kitchen', 'knife', 'professional', 'quality', 'stainless', 'steel'])]
            swedish_keywords = [k for k in keywords if any(word in k.lower() for word in ['kök', 'kniv', 'professionell', 'kvalitet', 'rostfritt', 'stål'])]
            
            analysis['keyword_analysis'] = {
                'total_count': len(keywords),
                'english_keywords': len(english_keywords),
                'swedish_keywords': len(swedish_keywords),
                'sample_english': english_keywords[:5],
                'sample_swedish': swedish_keywords[:5]
            }
            
            if swedish_keywords:
                analysis['successes'].append(f"✅ Swedish keywords generated: {len(swedish_keywords)}")
            if english_keywords:
                analysis['issues'].append(f"❌ English keywords found: {len(english_keywords)}")
    
    # Analyze A+ Content
    if 'aplus_content_plan' in listing:
        aplus = listing['aplus_content_plan']
        print(f"\n🖼️ A+ CONTENT ANALYSIS:")
        
        if isinstance(aplus, dict):
            sections = list(aplus.keys())
            print(f"Number of A+ sections: {len(sections)}")
            
            # Check each section
            for section_name, section_data in aplus.items():
                print(f"\nSection: {section_name}")
                if isinstance(section_data, dict):
                    if 'title' in section_data:
                        print(f"  Title: {section_data['title']}")
                    if 'content' in section_data:
                        content = section_data['content']
                        print(f"  Content length: {len(content)} characters")
                        
                        # Check language in A+ content
                        if any(word in content.lower() for word in ['kitchen', 'knife', 'professional', 'quality']):
                            analysis['issues'].append(f"❌ English in A+ section {section_name}")
                        if any(word in content.lower() for word in ['kök', 'kniv', 'professionell', 'kvalitet']):
                            analysis['successes'].append(f"✅ Swedish in A+ section {section_name}")
            
            analysis['aplus_analysis'] = {
                'sections_count': len(sections),
                'sections': list(sections)
            }
            
            if len(sections) >= 6:
                analysis['successes'].append(f"✅ Complete A+ content with {len(sections)} sections")
            else:
                analysis['issues'].append(f"❌ Incomplete A+ content: only {len(sections)} sections")
        else:
            analysis['issues'].append("❌ A+ content format invalid")
    else:
        analysis['issues'].append("❌ No A+ content generated")
    
    # Overall quality assessment
    total_issues = len(analysis['issues'])
    total_successes = len(analysis['successes'])
    
    if total_issues == 0:
        analysis['overall_quality'] = 'Excellent (10/10)'
    elif total_issues <= 2:
        analysis['overall_quality'] = 'Good (7-9/10)'
    elif total_issues <= 5:
        analysis['overall_quality'] = 'Fair (4-6/10)'
    else:
        analysis['overall_quality'] = 'Poor (1-3/10)'
    
    return analysis

def print_detailed_analysis(analysis):
    """Print detailed analysis results"""
    
    print(f"\n🎯 OVERALL QUALITY ASSESSMENT")
    print("=" * 50)
    print(f"Overall Quality: {analysis['overall_quality']}")
    print(f"Total Issues: {len(analysis['issues'])}")
    print(f"Total Successes: {len(analysis['successes'])}")
    
    if analysis['issues']:
        print(f"\n❌ ISSUES FOUND:")
        for issue in analysis['issues']:
            print(f"  {issue}")
    
    if analysis['successes']:
        print(f"\n✅ SUCCESSES:")
        for success in analysis['successes']:
            print(f"  {success}")
    
    # Language analysis summary
    if analysis['language_analysis']:
        print(f"\n🗣️ LANGUAGE ANALYSIS SUMMARY:")
        lang = analysis['language_analysis']
        
        if 'title' in lang:
            title_data = lang['title']
            print(f"  Title: {len(title_data.get('swedish_words', []))} Swedish words, {len(title_data.get('english_words', []))} English words")
        
        if 'bullets' in lang:
            print(f"  Bullets: {lang['bullets']['count']} generated")
    
    # Keywords analysis summary
    if analysis['keyword_analysis']:
        kw = analysis['keyword_analysis']
        print(f"\n🏷️ KEYWORDS SUMMARY:")
        print(f"  Total keywords: {kw['total_count']}")
        print(f"  Swedish keywords: {kw['swedish_keywords']}")
        print(f"  English keywords: {kw['english_keywords']}")
        
        if kw['sample_swedish']:
            print(f"  Sample Swedish: {', '.join(kw['sample_swedish'][:3])}")
        if kw['sample_english']:
            print(f"  Sample English: {', '.join(kw['sample_english'][:3])}")
    
    # A+ Content summary
    if analysis['aplus_analysis']:
        aplus = analysis['aplus_analysis']
        print(f"\n🖼️ A+ CONTENT SUMMARY:")
        print(f"  Sections generated: {aplus['sections_count']}")
        print(f"  Section names: {', '.join(aplus['sections'][:5])}")

def save_results(product, listing, analysis):
    """Save results to JSON file for review"""
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"sweden_listing_test_results_{timestamp}.json"
    
    results = {
        'timestamp': timestamp,
        'product': {
            'id': product.id,
            'name': product.name,
            'marketplace': product.marketplace,
            'language': product.marketplace_language
        },
        'listing': listing,
        'analysis': analysis
    }
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"\n💾 Results saved to: {filename}")
    except Exception as e:
        print(f"❌ Failed to save results: {e}")

def main():
    """Main test function"""
    
    print("🇸🇪 SWEDEN MARKETPLACE LISTING GENERATION TEST")
    print("=" * 60)
    
    # Step 1: Create test product
    print("\n1️⃣ Creating test product...")
    product = create_test_product()
    
    # Step 2: Generate listing
    print("\n2️⃣ Generating listing...")
    listing = generate_listing(product)
    
    # Step 3: Analyze quality
    print("\n3️⃣ Analyzing listing quality...")
    analysis = analyze_listing_quality(listing)
    
    # Step 4: Print results
    print_detailed_analysis(analysis)
    
    # Step 5: Save results
    save_results(product, listing, analysis)
    
    print(f"\n🏁 TEST COMPLETED")
    print("=" * 60)
    
    return {
        'product': product,
        'listing': listing,
        'analysis': analysis
    }

if __name__ == "__main__":
    results = main()