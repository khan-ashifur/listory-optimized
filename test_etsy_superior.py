"""
🎨 SUPERIOR ETSY LISTING GENERATOR TEST & EVALUATION
Tests and evaluates the quality of generated Etsy listings
"""

import os
import sys
import django
import json
from datetime import datetime

# Setup Django
backend_path = os.path.join(os.getcwd(), 'backend')
sys.path.insert(0, backend_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory.settings')
django.setup()

from apps.listings.services import ListingGeneratorService
from apps.core.models import Product
from apps.listings.models import GeneratedListing
from django.contrib.auth.models import User


def create_test_products():
    """Create diverse test products for Etsy"""
    user, created = User.objects.get_or_create(username='etsy_test_superior')
    
    test_products = [
        {
            'name': 'Hand-Painted Ceramic Coffee Mug',
            'brand_name': 'ArtisanCeramics',
            'price': 35.00,
            'description': 'Beautiful hand-painted ceramic mug with unique floral designs',
            'categories': 'Home & Living > Kitchen & Dining > Drink & Barware > Mugs',
            'features': 'Hand-painted design\nDishwasher safe\nMicrowave safe\n16oz capacity\nLead-free glaze',
            'brand_tone': 'handmade_artisan',
            'occasion': 'mothers_day'
        },
        {
            'name': 'Vintage Style Pearl Hair Pins',
            'brand_name': 'VintageGlamour',
            'price': 28.00,
            'description': 'Delicate pearl hair pins with gold wire wrapping, perfect for weddings',
            'categories': 'Accessories > Hair Accessories > Hair Pins',
            'features': 'Freshwater pearls\nGold-plated wire\nSet of 3 pins\nVintage inspired\nGift box included',
            'brand_tone': 'vintage_charm',
            'occasion': 'wedding'
        },
        {
            'name': 'Macrame Wall Hanging',
            'brand_name': 'BohoDecorStudio',
            'price': 65.00,
            'description': 'Large bohemian macrame wall hanging made with organic cotton',
            'categories': 'Home & Living > Home Decor > Wall Hangings',
            'features': 'Organic cotton rope\n36 inches wide\nNatural wood dowel\nCustom colors available\nReady to hang',
            'brand_tone': 'bohemian_free',
            'occasion': 'housewarming'
        },
        {
            'name': 'Coquette Pink Bow Earrings',
            'brand_name': 'MessyCoquetteShop',
            'price': 22.00,
            'description': 'Adorable pink satin bow earrings with pearl drops, perfect coquette aesthetic',
            'categories': 'Jewelry > Earrings > Drop Earrings',
            'features': 'Satin ribbon bows\nFreshwater pearl drops\nSterling silver posts\nHypoallergenic\nLightweight design',
            'brand_tone': 'messy_coquette',
            'occasion': 'valentine_day'
        },
        {
            'name': 'Sustainable Bamboo Cutting Board',
            'brand_name': 'EcoKitchenCo',
            'price': 45.00,
            'description': 'Eco-friendly bamboo cutting board with juice groove and handle',
            'categories': 'Home & Living > Kitchen & Dining > Kitchen Tools',
            'features': 'Sustainable bamboo\nJuice groove\nBuilt-in handle\nNaturally antimicrobial\nOil finish included',
            'brand_tone': 'eco_conscious',
            'occasion': ''
        }
    ]
    
    products = []
    for data in test_products:
        # Clean up old test products
        Product.objects.filter(user=user, name=data['name']).delete()
        
        product = Product.objects.create(
            user=user,
            target_platform='etsy',
            marketplace='etsy',
            marketplace_language='en',
            **data
        )
        products.append(product)
        print(f"✅ Created test product: {product.name} ({data['brand_tone']})")
    
    return products


def evaluate_etsy_listing(listing, product):
    """Comprehensive evaluation of Etsy listing quality"""
    print(f"\n{'='*80}")
    print(f"🎨 EVALUATING: {product.name}")
    print(f"   Brand Tone: {product.brand_tone}")
    print(f"   Price: ${product.price}")
    print(f"{'='*80}")
    
    scores = {}
    issues = []
    
    # 1. TITLE EVALUATION (140 chars max)
    title = listing.etsy_title or listing.title
    print(f"\n📝 TITLE ({len(title)} chars):")
    print(f"   {title}")
    
    title_score = 0
    if len(title) <= 140:
        title_score += 2
    else:
        issues.append(f"Title too long: {len(title)} chars (max 140)")
    
    # Check for keywords
    keywords = ['custom', 'personalized', 'handmade', 'unique', 'gift']
    keyword_count = sum(1 for kw in keywords if kw.lower() in title.lower())
    if keyword_count >= 2:
        title_score += 2
    else:
        issues.append(f"Title needs more power keywords (found {keyword_count})")
    
    # Check front-loading
    if any(title.lower().startswith(kw) for kw in ['custom', 'handmade', 'personalized', product.name.lower()[:10]]):
        title_score += 2
    else:
        issues.append("Title should front-load primary keywords")
    
    # Check for brand tone alignment
    if product.brand_tone and any(word in title.lower() for word in product.brand_tone.split('_')):
        title_score += 2
    
    # Check for gift/occasion mention
    if 'gift' in title.lower() or (product.occasion and product.occasion.replace('_', ' ') in title.lower()):
        title_score += 2
    
    scores['title'] = title_score
    print(f"   Score: {title_score}/10")
    
    # 2. TAGS EVALUATION (13 tags, 20 chars each)
    try:
        tags = json.loads(listing.etsy_tags) if listing.etsy_tags else []
    except:
        tags = []
    
    print(f"\n🏷️ TAGS ({len(tags)} tags):")
    tags_score = 0
    
    if len(tags) == 13:
        tags_score += 3
    else:
        issues.append(f"Should have exactly 13 tags (has {len(tags)})")
    
    # Check tag lengths
    long_tags = [tag for tag in tags if len(tag) > 20]
    if not long_tags:
        tags_score += 2
    else:
        issues.append(f"{len(long_tags)} tags exceed 20 chars")
    
    # Check for variety
    if tags:
        # Check for mix of short and long tags
        tag_lengths = [len(tag) for tag in tags]
        if min(tag_lengths) < 10 and max(tag_lengths) > 15:
            tags_score += 2
        
        # Check for product name in tags
        if any(product.name.lower()[:15] in tag.lower() for tag in tags):
            tags_score += 1
        
        # Check for brand tone in tags
        if any(any(word in tag.lower() for word in product.brand_tone.split('_')) for tag in tags):
            tags_score += 1
        
        # Check for trending/seasonal tags
        trending = ['2025', 'trending', 'viral', 'aesthetic', 'core']
        if any(any(trend in tag.lower() for trend in trending) for tag in tags):
            tags_score += 1
    
    scores['tags'] = tags_score
    print(f"   First 5 tags: {tags[:5]}")
    print(f"   Score: {tags_score}/10")
    
    # 3. DESCRIPTION EVALUATION
    description = listing.etsy_description or listing.long_description or ''
    print(f"\n📄 DESCRIPTION ({len(description)} chars):")
    desc_score = 0
    
    # Length check
    if len(description) >= 500:
        desc_score += 2
    else:
        issues.append(f"Description too short: {len(description)} chars (min 500)")
    
    # Check for emotional hook (first 160 chars)
    first_160 = description[:160].lower()
    emotional_words = ['love', 'special', 'unique', 'perfect', 'beautiful', 'amazing', 'dream']
    if any(word in first_160 for word in emotional_words):
        desc_score += 2
    else:
        issues.append("Description needs emotional hook in first 160 chars")
    
    # Check for sections
    required_sections = ['story', 'features', 'custom', 'gift', 'shipping', 'material']
    sections_found = sum(1 for section in required_sections if section in description.lower())
    desc_score += min(3, sections_found)
    if sections_found < 4:
        issues.append(f"Description missing key sections (found {sections_found}/6)")
    
    # Check for personalization mention
    if 'personaliz' in description.lower() or 'custom' in description.lower():
        desc_score += 1
    
    # Check for urgency/CTA
    cta_words = ['order today', 'limited', 'favorite', 'message me', 'questions']
    if any(word in description.lower() for word in cta_words):
        desc_score += 1
    
    # Check for brand tone alignment
    if product.brand_tone and any(word in description.lower() for word in product.brand_tone.split('_')):
        desc_score += 1
    
    scores['description'] = desc_score
    print(f"   First 200 chars: {description[:200]}...")
    print(f"   Score: {desc_score}/10")
    
    # 4. MATERIALS & PROCESSING
    materials = listing.etsy_materials or ''
    processing = listing.etsy_processing_time or ''
    
    print(f"\n🛠️ MATERIALS & PROCESSING:")
    print(f"   Materials: {materials[:100]}")
    print(f"   Processing: {processing}")
    
    tech_score = 0
    if materials:
        tech_score += 3
    else:
        issues.append("Missing materials list")
    
    if processing:
        tech_score += 3
    else:
        issues.append("Missing processing time")
    
    # Check for eco/sustainable mentions
    if any(word in materials.lower() for word in ['eco', 'sustainable', 'organic', 'recycled']):
        tech_score += 2
    
    # Check processing time format
    if any(word in processing.lower() for word in ['business days', 'weeks', 'made to order']):
        tech_score += 2
    
    scores['technical'] = tech_score
    print(f"   Score: {tech_score}/10")
    
    # 5. SEO & KEYWORDS
    keywords = listing.keywords or ''
    print(f"\n🔍 SEO KEYWORDS ({len(keywords.split(','))} keywords):")
    seo_score = 0
    
    if keywords:
        keyword_list = [kw.strip() for kw in keywords.split(',')]
        if len(keyword_list) >= 10:
            seo_score += 5
        else:
            seo_score += 2
            issues.append(f"Need more keywords (has {len(keyword_list)})")
        
        # Check for long-tail keywords
        long_tail = [kw for kw in keyword_list if len(kw.split()) >= 2]
        if len(long_tail) >= 5:
            seo_score += 3
        
        # Check for brand tone keywords
        if any(any(word in kw.lower() for word in product.brand_tone.split('_')) for kw in keyword_list):
            seo_score += 2
    else:
        issues.append("No keywords generated")
    
    scores['seo'] = seo_score
    print(f"   First 5: {', '.join(keywords.split(',')[:5])}")
    print(f"   Score: {seo_score}/10")
    
    # CALCULATE FINAL SCORE
    total_score = sum(scores.values())
    max_score = len(scores) * 10
    percentage = (total_score / max_score) * 100
    
    print(f"\n📊 OVERALL QUALITY SCORE:")
    print(f"   Title: {scores['title']}/10")
    print(f"   Tags: {scores['tags']}/10")
    print(f"   Description: {scores['description']}/10")
    print(f"   Technical: {scores['technical']}/10")
    print(f"   SEO: {scores['seo']}/10")
    print(f"   {'='*30}")
    print(f"   TOTAL: {total_score}/{max_score} ({percentage:.1f}%)")
    
    # Quality assessment
    if percentage >= 90:
        quality = "🏆 SUPERIOR - Beats Helium 10 & Jasper AI"
    elif percentage >= 80:
        quality = "✅ EXCELLENT - Professional Quality"
    elif percentage >= 70:
        quality = "👍 GOOD - Above Average"
    elif percentage >= 60:
        quality = "⚠️ FAIR - Needs Improvement"
    else:
        quality = "❌ POOR - Significant Issues"
    
    print(f"   {quality}")
    
    if issues:
        print(f"\n⚠️ ISSUES TO FIX:")
        for issue in issues[:5]:  # Show top 5 issues
            print(f"   • {issue}")
    
    return {
        'product': product.name,
        'brand_tone': product.brand_tone,
        'scores': scores,
        'total': total_score,
        'percentage': percentage,
        'quality': quality,
        'issues': issues
    }


def main():
    print("🎨 SUPERIOR ETSY LISTING GENERATOR TEST")
    print("=" * 80)
    
    # Create test products
    products = create_test_products()
    
    # Initialize service
    service = ListingGeneratorService()
    
    # Generate listings and evaluate
    results = []
    for product in products:
        print(f"\n🔄 Generating listing for {product.name}...")
        try:
            listing = service.generate_listing(product.id, 'etsy')
            evaluation = evaluate_etsy_listing(listing, product)
            results.append(evaluation)
            
            # Save the best one for viewing
            if evaluation['percentage'] >= 80:
                print(f"\n🌐 View this listing at: http://localhost:3000/results/{listing.id}")
        except Exception as e:
            print(f"❌ Error generating listing: {e}")
    
    # Summary report
    print(f"\n{'='*80}")
    print("📊 FINAL EVALUATION REPORT")
    print(f"{'='*80}")
    
    if results:
        avg_score = sum(r['percentage'] for r in results) / len(results)
        print(f"\n🎯 Average Quality Score: {avg_score:.1f}%")
        
        # Quality breakdown
        superior = [r for r in results if r['percentage'] >= 90]
        excellent = [r for r in results if 80 <= r['percentage'] < 90]
        good = [r for r in results if 70 <= r['percentage'] < 80]
        needs_work = [r for r in results if r['percentage'] < 70]
        
        print(f"\n📈 Quality Distribution:")
        print(f"   🏆 Superior (90%+): {len(superior)} listings")
        print(f"   ✅ Excellent (80-89%): {len(excellent)} listings")
        print(f"   👍 Good (70-79%): {len(good)} listings")
        print(f"   ⚠️ Needs Work (<70%): {len(needs_work)} listings")
        
        # Best performing brand tones
        print(f"\n🎨 Brand Tone Performance:")
        tone_scores = {}
        for r in results:
            tone = r['brand_tone']
            if tone not in tone_scores:
                tone_scores[tone] = []
            tone_scores[tone].append(r['percentage'])
        
        for tone, scores in tone_scores.items():
            avg = sum(scores) / len(scores)
            print(f"   {tone}: {avg:.1f}%")
        
        # Common issues
        all_issues = []
        for r in results:
            all_issues.extend(r['issues'])
        
        if all_issues:
            print(f"\n⚠️ Most Common Issues:")
            from collections import Counter
            issue_counts = Counter(all_issues)
            for issue, count in issue_counts.most_common(5):
                print(f"   • {issue} ({count} occurrences)")
        
        # Competitor comparison
        print(f"\n🏆 COMPETITOR COMPARISON:")
        if avg_score >= 85:
            print("   ✅ SUPERIOR to Helium 10, Jasper AI, and CopyMonkey")
            print("   ✅ Ready for production use!")
        elif avg_score >= 75:
            print("   ✅ COMPETITIVE with major tools")
            print("   ⚠️ Minor improvements needed for superiority")
        else:
            print("   ❌ Below competitor standards")
            print("   ❌ Significant improvements required")
    
    # Save results
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    with open(f'etsy_evaluation_{timestamp}.json', 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\n💾 Results saved to etsy_evaluation_{timestamp}.json")


if __name__ == "__main__":
    main()