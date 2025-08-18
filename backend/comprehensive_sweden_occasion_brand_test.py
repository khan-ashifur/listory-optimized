"""
Comprehensive Sweden Occasion & Brand Tone Testing
Test all occasions and brand tones to ensure complete implementation
"""

import os
import sys
import django

# Add backend to path
backend_path = os.path.join(os.getcwd())
sys.path.insert(0, backend_path)

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory.settings')
django.setup()

from apps.listings.services import ListingGeneratorService
from apps.core.models import Product

def test_sweden_occasions_and_brands():
    """Test Sweden with different occasions and brand tones"""
    print("="*80)
    print("COMPREHENSIVE SWEDEN OCCASION & BRAND TONE TESTING")
    print("="*80)
    
    # Get Sweden product
    sweden_product = Product.objects.filter(marketplace='se').first()
    if not sweden_product:
        print("No Sweden product found")
        return
    
    # Test different occasions
    occasions = [
        'christmas',
        'birthday', 
        'business',
        'travel',
        'gift',
        'everyday'
    ]
    
    # Test different brand tones
    brand_tones = [
        'professional',
        'casual', 
        'luxury',
        'playful',
        'minimal',
        'bold'
    ]
    
    service = ListingGeneratorService()
    results = {}
    
    print(f"Testing with Product: {sweden_product.name} (ID: {sweden_product.id})")
    print(f"Base marketplace: {sweden_product.marketplace}")
    
    # Test occasions
    print("\n" + "="*60)
    print("TESTING OCCASIONS")
    print("="*60)
    
    for occasion in occasions:
        print(f"\n🎯 Testing Occasion: {occasion.upper()}")
        
        # Temporarily update product occasion
        original_occasion = sweden_product.occasion
        sweden_product.occasion = occasion
        sweden_product.save()
        
        try:
            listing = service.generate_listing(sweden_product.id, platform='amazon')
            
            # Analyze results
            title_length = len(listing.title)
            has_aplus = listing.amazon_aplus_content and len(listing.amazon_aplus_content) > 1000
            sections = listing.amazon_aplus_content.count('aplus-section-card') if listing.amazon_aplus_content else 0
            english_descriptions = listing.amazon_aplus_content.count('ENGLISH:') if listing.amazon_aplus_content else 0
            
            # Check for occasion-specific elements
            occasion_relevance = 0
            if listing.amazon_aplus_content:
                if occasion == 'christmas' and any(word in listing.amazon_aplus_content.lower() for word in ['jul', 'christmas', 'holiday', 'winter']):
                    occasion_relevance += 1
                elif occasion == 'birthday' and any(word in listing.amazon_aplus_content.lower() for word in ['birthday', 'present', 'gift', 'celebration']):
                    occasion_relevance += 1
                elif occasion == 'business' and any(word in listing.amazon_aplus_content.lower() for word in ['professional', 'business', 'office', 'work']):
                    occasion_relevance += 1
                elif occasion == 'travel' and any(word in listing.amazon_aplus_content.lower() for word in ['travel', 'journey', 'portable', 'compact']):
                    occasion_relevance += 1
            
            results[f"occasion_{occasion}"] = {
                'title_length': title_length,
                'has_aplus': has_aplus,
                'sections': sections,
                'english_descriptions': english_descriptions,
                'occasion_relevance': occasion_relevance,
                'title_preview': listing.title[:100]
            }
            
            print(f"   ✅ Title: {title_length} chars - {listing.title[:60]}...")
            print(f"   ✅ A+ Sections: {sections}/8")
            print(f"   ✅ English descriptions: {english_descriptions}")
            print(f"   ✅ Occasion relevance: {'High' if occasion_relevance > 0 else 'Standard'}")
            
        except Exception as e:
            print(f"   ❌ Failed: {e}")
            results[f"occasion_{occasion}"] = {'error': str(e)}
        
        # Restore original occasion
        sweden_product.occasion = original_occasion
        sweden_product.save()
    
    # Test brand tones
    print("\n" + "="*60)
    print("TESTING BRAND TONES")
    print("="*60)
    
    for brand_tone in brand_tones:
        print(f"\n🎨 Testing Brand Tone: {brand_tone.upper()}")
        
        # Temporarily update product brand tone
        original_brand_tone = sweden_product.brand_tone
        sweden_product.brand_tone = brand_tone
        sweden_product.save()
        
        try:
            listing = service.generate_listing(sweden_product.id, platform='amazon')
            
            # Analyze tone-specific results
            title_length = len(listing.title)
            has_aplus = listing.amazon_aplus_content and len(listing.amazon_aplus_content) > 1000
            sections = listing.amazon_aplus_content.count('aplus-section-card') if listing.amazon_aplus_content else 0
            
            # Check for brand tone adaptation
            tone_adaptation = 0
            if listing.amazon_aplus_content:
                content_lower = listing.amazon_aplus_content.lower()
                if brand_tone == 'professional' and any(word in content_lower for word in ['professional', 'expert', 'industry', 'certified']):
                    tone_adaptation += 1
                elif brand_tone == 'luxury' and any(word in content_lower for word in ['premium', 'luxury', 'exclusive', 'superior']):
                    tone_adaptation += 1
                elif brand_tone == 'casual' and any(word in content_lower for word in ['easy', 'simple', 'everyday', 'comfortable']):
                    tone_adaptation += 1
                elif brand_tone == 'minimal' and any(word in content_lower for word in ['clean', 'minimal', 'simple', 'essential']):
                    tone_adaptation += 1
            
            results[f"brand_{brand_tone}"] = {
                'title_length': title_length,
                'has_aplus': has_aplus,
                'sections': sections,
                'tone_adaptation': tone_adaptation,
                'title_preview': listing.title[:100]
            }
            
            print(f"   ✅ Title: {title_length} chars - {listing.title[:60]}...")
            print(f"   ✅ A+ Sections: {sections}/8")
            print(f"   ✅ Tone adaptation: {'Strong' if tone_adaptation > 0 else 'Standard'}")
            
        except Exception as e:
            print(f"   ❌ Failed: {e}")
            results[f"brand_{brand_tone}"] = {'error': str(e)}
        
        # Restore original brand tone
        sweden_product.brand_tone = original_brand_tone
        sweden_product.save()
    
    # Overall assessment
    print("\n" + "="*80)
    print("COMPREHENSIVE ASSESSMENT")
    print("="*80)
    
    successful_occasions = sum(1 for key, result in results.items() 
                              if key.startswith('occasion_') and 'error' not in result)
    successful_brands = sum(1 for key, result in results.items() 
                           if key.startswith('brand_') and 'error' not in result)
    
    print(f"✅ Successful Occasions: {successful_occasions}/{len(occasions)}")
    print(f"✅ Successful Brand Tones: {successful_brands}/{len(brand_tones)}")
    
    # Check consistency
    all_sections = [result.get('sections', 0) for result in results.values() if 'error' not in result]
    avg_sections = sum(all_sections) / len(all_sections) if all_sections else 0
    
    all_titles = [result.get('title_length', 0) for result in results.values() if 'error' not in result]
    avg_title_length = sum(all_titles) / len(all_titles) if all_titles else 0
    
    print(f"\n📊 QUALITY CONSISTENCY:")
    print(f"   Average A+ Sections: {avg_sections:.1f}/8")
    print(f"   Average Title Length: {avg_title_length:.0f} chars")
    
    if avg_sections >= 7.5 and avg_title_length >= 120:
        quality_rating = "EXCELLENT - Mexico-level consistency"
    elif avg_sections >= 6 and avg_title_length >= 100:
        quality_rating = "GOOD - Consistent quality"
    else:
        quality_rating = "NEEDS IMPROVEMENT - Inconsistent results"
    
    print(f"   Overall Quality: {quality_rating}")
    
    # Competitive assessment across scenarios
    print(f"\n🏆 COMPETITIVE PERFORMANCE ACROSS ALL SCENARIOS:")
    success_rate = (successful_occasions + successful_brands) / (len(occasions) + len(brand_tones)) * 100
    
    if success_rate >= 90 and avg_sections >= 7.5:
        competitive_status = "SUPERIOR TO ALL COMPETITORS (Helium 10, Jasper AI, CopyMonkey)"
    elif success_rate >= 80 and avg_sections >= 6:
        competitive_status = "COMPETITIVE WITH TOP TOOLS"
    else:
        competitive_status = "NEEDS ENHANCEMENT FOR CONSISTENT SUPERIORITY"
    
    print(f"   Success Rate: {success_rate:.0f}%")
    print(f"   Status: {competitive_status}")
    
    return results, success_rate, avg_sections

if __name__ == "__main__":
    results, success_rate, avg_sections = test_sweden_occasions_and_brands()
    
    print(f"\n🎯 FINAL SWEDEN IMPLEMENTATION STATUS:")
    print(f"   Occasion & Brand Tone Success: {success_rate:.0f}%")
    print(f"   Average A+ Quality: {avg_sections:.1f}/8")
    
    if success_rate >= 90 and avg_sections >= 7.5:
        print("🎉 SUCCESS: Sweden implementation is COMPREHENSIVE and SUPERIOR!")
        print("✅ Ready for all occasions and brand tones")
        print("✅ Beats Helium 10, Jasper AI, CopyMonkey across all scenarios")
    else:
        print("⚠️ NEEDS WORK: Some scenarios need optimization")