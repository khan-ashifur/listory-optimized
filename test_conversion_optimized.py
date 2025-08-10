"""
Test script to verify conversion-optimized improvements
Evaluates listing quality based on e-commerce best practices
"""

import os
import sys
import django
import json
import re

# Add the backend directory to the Python path
sys.path.insert(0, 'C:/Users/khana/Desktop/listory-ai/backend')

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory.settings')
django.setup()

from apps.core.models import Product
from apps.listings.services import ListingGeneratorService
from django.contrib.auth.models import User

def evaluate_listing_quality(data):
    """Evaluate listing based on e-commerce best practices"""
    scores = {}
    
    # 1. Title evaluation
    title = data.get('productTitle', '')
    title_lower = title.lower()
    
    # Check if keywords come first (not brand)
    brand_position = title_lower.find('coolbreeze') if 'coolbreeze' in title_lower else len(title)
    keyword_position = min(title_lower.find('neck fan') if 'neck fan' in title_lower else 999,
                          title_lower.find('portable') if 'portable' in title_lower else 999)
    scores['keywords_first'] = 10 if keyword_position < brand_position else 5
    
    # Check for benefit in first 60 chars
    first_60 = title[:60]
    benefit_words = ['cooling', 'relief', 'stronger', 'longer', 'instant', 'powerful']
    scores['benefit_early'] = 10 if any(word in first_60.lower() for word in benefit_words) else 5
    
    # 2. Bullet evaluation
    bullets = data.get('bulletPoints', [])
    
    # Check for labels
    label_count = sum(1 for bullet in bullets if ':' in bullet[:50])
    scores['bullet_labels'] = (label_count / 5) * 10 if bullets else 0
    
    # Check benefit-first structure
    benefit_first_count = 0
    for bullet in bullets:
        # Check if benefit words appear before technical specs
        if bullet:
            first_part = bullet[:100].lower()
            if any(word in first_part for word in ['instant', 'enjoy', 'relief', 'comfort', 'easy', 'no more']):
                benefit_first_count += 1
    scores['benefit_first'] = (benefit_first_count / 5) * 10 if bullets else 0
    
    # 3. Description evaluation
    description = data.get('productDescription', '')
    
    # Check for quick benefit list
    scores['quick_list'] = 10 if '•' in description[:400] or '✓' in description[:400] else 5
    
    # Check for seasonal keywords
    seasonal_words = ['summer', 'gift', 'hot weather', 'outdoor', 'vacation', 'beach']
    seasonal_count = sum(1 for word in seasonal_words if word in description.lower())
    scores['seasonal_keywords'] = min(seasonal_count * 2, 10)
    
    # 4. Overall keyword variety
    all_text = title + ' '.join(bullets[:2]) if bullets else title
    unique_keywords = set()
    keyword_patterns = ['fan', 'cool', 'portable', 'neck', 'usb', 'battery', 'travel', 'outdoor']
    for pattern in keyword_patterns:
        if pattern in all_text.lower():
            unique_keywords.add(pattern)
    scores['keyword_variety'] = min(len(unique_keywords) * 1.5, 10)
    
    # 5. Social proof
    social_proof_patterns = [r'\d+,?\d* customers', r'\d+,?\d* sold', r'\d+\.\d+ star', r'\d+% satisfaction']
    social_proof_found = any(re.search(pattern, all_text) for pattern in social_proof_patterns)
    scores['social_proof'] = 10 if social_proof_found else 5
    
    return scores

def test_conversion_optimization():
    """Test the conversion-focused improvements"""
    
    # Get or create test user
    user, _ = User.objects.get_or_create(username='test_user')
    
    # Test product configuration
    test_product_data = {
        'name': 'Neck Fan Portable',
        'description': 'Powerful bladeless neck fan with 360° airflow. 12-hour battery life, 3 speeds, ultra-quiet operation. Perfect for outdoor work, travel, sports, and hot summer days.',
        'brand_name': 'CoolBreeze',
        'brand_tone': 'casual',
        'target_platform': 'amazon',
        'price': 39.99,
        'categories': 'Electronics, Portable Fans, Travel Accessories, Summer Essentials',
        'features': '360° airflow, 12-hour battery, 3 speeds, USB-C charging, 180g lightweight, Adjustable band',
        'target_keywords': 'neck fan, portable fan, personal fan, hands free fan, wearable fan',
        'occasion': 'summer'
    }
    
    service = ListingGeneratorService()
    
    print("\n" + "="*80)
    print("TESTING CONVERSION-OPTIMIZED IMPROVEMENTS")
    print("="*80)
    
    # Create test product
    product = Product.objects.create(
        user=user,
        marketplace='us',
        marketplace_language='en',
        **test_product_data
    )
    
    try:
        # Generate listing
        listing = service._generate_amazon_listing(product, None)
        
        # Parse the response
        if hasattr(listing, 'amazon_data') and listing.amazon_data:
            data = json.loads(listing.amazon_data) if isinstance(listing.amazon_data, str) else listing.amazon_data
            
            print(f"\n📊 GENERATED LISTING PREVIEW:")
            print(f"{'='*60}")
            
            # Show title
            title = data.get('productTitle', 'No title generated')
            print(f"\n📌 TITLE (First 80 chars shown):")
            print(f"   {title[:80]}...")
            
            # Show first 2 bullets
            print(f"\n🎯 BULLETS (First 2 shown):")
            bullets = data.get('bulletPoints', [])
            for i, bullet in enumerate(bullets[:2], 1):
                print(f"\n   Bullet {i}:")
                # Show label separately
                if ':' in bullet:
                    label, content = bullet.split(':', 1)
                    print(f"   LABEL: {label}:")
                    print(f"   CONTENT: {content[:100]}...")
                else:
                    print(f"   {bullet[:120]}...")
            
            # Show description opening
            print(f"\n📝 DESCRIPTION (Quick list section):")
            description = data.get('productDescription', '')
            if description:
                first_part = description[:400]
                print(f"   {first_part}...")
            
            # Evaluate quality
            print(f"\n" + "="*60)
            print(f"🏆 E-COMMERCE SPECIALIST EVALUATION:")
            print(f"="*60)
            
            scores = evaluate_listing_quality(data)
            total_score = sum(scores.values()) / len(scores)
            
            for metric, score in scores.items():
                emoji = "✅" if score >= 8 else "⚠️" if score >= 6 else "❌"
                metric_name = metric.replace('_', ' ').title()
                print(f"{emoji} {metric_name}: {score}/10")
            
            print(f"\n{'='*40}")
            overall_emoji = "🏆" if total_score >= 8 else "📈" if total_score >= 6 else "⚠️"
            print(f"{overall_emoji} OVERALL SCORE: {total_score:.1f}/10")
            
            # Recommendations
            if total_score < 8:
                print(f"\n📋 RECOMMENDATIONS:")
                if scores['keywords_first'] < 8:
                    print("   • Move high-volume keywords before brand name")
                if scores['benefit_early'] < 8:
                    print("   • Add stronger benefit claim in first 60 chars")
                if scores['bullet_labels'] < 8:
                    print("   • Add clear LABEL: format to all bullets")
                if scores['seasonal_keywords'] < 8:
                    print("   • Include more seasonal/gift keywords")
            
    except Exception as e:
        print(f"   ❌ Error generating listing: {str(e)}")
    
    finally:
        # Clean up test product
        product.delete()
    
    print("\n" + "="*80)
    print("✅ CONVERSION OPTIMIZATION TEST COMPLETE")
    print("="*80)

if __name__ == "__main__":
    test_conversion_optimization()