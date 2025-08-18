#!/usr/bin/env python
"""
Compare Sweden A+ content structure with Mexico (10/10 standard)
"""
import os
import sys
import django
import json
import re

# Add backend directory to path
sys.path.insert(0, 'C:/Users/khana/Desktop/listory-ai/backend')

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory.settings')
django.setup()

from apps.listings.models import GeneratedListing

def compare_sweden_mexico_aplus():
    """Compare Sweden A+ content with Mexico's 10/10 standard"""
    
    # Get latest Sweden listing
    sweden_listing = GeneratedListing.objects.filter(
        product__marketplace='se',
        amazon_aplus_content__isnull=False
    ).exclude(amazon_aplus_content='').order_by('-created_at').first()
    
    # Get latest Mexico listing for comparison
    mexico_listing = GeneratedListing.objects.filter(
        product__marketplace='mx',
        amazon_aplus_content__isnull=False
    ).exclude(amazon_aplus_content='').order_by('-created_at').first()
    
    print(f"🇸🇪 vs 🇲🇽 A+ CONTENT COMPARISON")
    print(f"=" * 60)
    
    if sweden_listing:
        print(f"Sweden Listing: {sweden_listing.id} (Quality: {sweden_listing.quality_score})")
    else:
        print("Sweden Listing: Not found")
        
    if mexico_listing:
        print(f"Mexico Listing: {mexico_listing.id} (Quality: {mexico_listing.quality_score})")
    else:
        print("Mexico Listing: Not found")
    
    if not sweden_listing or not mexico_listing:
        print("Cannot compare - missing listings")
        return
    
    # Analyze A+ content structure
    def analyze_aplus_structure(content, country):
        print(f"\n🎨 {country.upper()} A+ CONTENT ANALYSIS")
        print(f"=" * 40)
        
        if content.strip().startswith('{'):
            try:
                aplus_data = json.loads(content)
                print("Format: JSON ✅")
                
                if 'aPlusContentPlan' in aplus_data:
                    plan = aplus_data['aPlusContentPlan']
                    print(f"Sections: {len(plan)}")
                    
                    # Expected sections for 10/10 quality
                    expected_sections = [
                        'section1_hero', 'section2_features', 'section3_usage',
                        'section4_quality', 'section5_guarantee', 'section6_social_proof',
                        'section7_comparison', 'section8_package'
                    ]
                    
                    found_sections = list(plan.keys())
                    print(f"Found sections: {found_sections}")
                    
                    # Check section completeness
                    section_score = 0
                    for section in expected_sections:
                        if any(section in found for found in found_sections):
                            section_score += 1
                    
                    print(f"Section completeness: {section_score}/{len(expected_sections)} ({section_score/len(expected_sections)*100:.1f}%)")
                    
                    # Analyze section quality
                    total_content_length = 0
                    sections_with_content = 0
                    
                    for section_name, section_data in plan.items():
                        print(f"\n  📍 {section_name}:")
                        
                        if 'title' in section_data:
                            title = section_data['title']
                            print(f"    Title: {title[:60]}...")
                            print(f"    Title length: {len(title)} chars")
                        
                        if 'content' in section_data:
                            content_text = section_data['content']
                            total_content_length += len(content_text)
                            sections_with_content += 1
                            print(f"    Content: {content_text[:80]}...")
                            print(f"    Content length: {len(content_text)} chars")
                        
                        if 'imageDescription' in section_data:
                            img_desc = section_data['imageDescription']
                            is_english = any(word in img_desc.lower() for word in ['image', 'photo', 'showing', 'professional'])
                            print(f"    Image desc: {'English ✅' if is_english else 'Non-English ❌'}")
                        
                        # Check for features/benefits arrays
                        for key in ['features', 'trust_builders', 'use_cases', 'advantages', 'faqs']:
                            if key in section_data and isinstance(section_data[key], list):
                                print(f"    {key}: {len(section_data[key])} items")
                    
                    avg_content_length = total_content_length / sections_with_content if sections_with_content > 0 else 0
                    print(f"\nOverall metrics:")
                    print(f"  Total content length: {total_content_length} chars")
                    print(f"  Average per section: {avg_content_length:.0f} chars")
                    print(f"  Sections with content: {sections_with_content}")
                    
                    return {
                        'format': 'JSON',
                        'section_count': len(plan),
                        'section_completeness': section_score/len(expected_sections),
                        'total_content_length': total_content_length,
                        'avg_section_length': avg_content_length,
                        'sections_with_content': sections_with_content
                    }
                
            except Exception as e:
                print(f"JSON parsing error: {e}")
                return {'format': 'JSON_ERROR', 'error': str(e)}
        else:
            # HTML content
            print("Format: HTML")
            print(f"Content length: {len(content)} chars")
            
            # Count sections in HTML
            section_count = len(re.findall(r'<div[^>]*class[^>]*aplus[^>]*>', content))
            print(f"HTML sections found: {section_count}")
            
            return {
                'format': 'HTML',
                'section_count': section_count,
                'total_content_length': len(content)
            }
    
    # Analyze both countries
    sweden_analysis = analyze_aplus_structure(sweden_listing.amazon_aplus_content, "Sweden")
    mexico_analysis = analyze_aplus_structure(mexico_listing.amazon_aplus_content, "Mexico")
    
    # Comparison
    print(f"\n🏆 COMPARATIVE ANALYSIS")
    print(f"=" * 40)
    
    if sweden_analysis and mexico_analysis:
        print(f"Format: Sweden {sweden_analysis['format']} vs Mexico {mexico_analysis['format']}")
        print(f"Sections: Sweden {sweden_analysis['section_count']} vs Mexico {mexico_analysis['section_count']}")
        
        if 'total_content_length' in sweden_analysis and 'total_content_length' in mexico_analysis:
            print(f"Content volume: Sweden {sweden_analysis['total_content_length']} vs Mexico {mexico_analysis['total_content_length']} chars")
        
        if 'section_completeness' in sweden_analysis and 'section_completeness' in mexico_analysis:
            sweden_completeness = sweden_analysis['section_completeness'] * 100
            mexico_completeness = mexico_analysis['section_completeness'] * 100
            print(f"Completeness: Sweden {sweden_completeness:.1f}% vs Mexico {mexico_completeness:.1f}%")
        
        # Winner determination
        sweden_score = sweden_analysis.get('section_count', 0) + sweden_analysis.get('total_content_length', 0) / 1000
        mexico_score = mexico_analysis.get('section_count', 0) + mexico_analysis.get('total_content_length', 0) / 1000
        
        if sweden_score > mexico_score:
            print(f"🏆 Sweden has more comprehensive A+ content")
        elif mexico_score > sweden_score:
            print(f"🏆 Mexico has more comprehensive A+ content")
        else:
            print(f"🤝 Both countries have similar A+ content volume")
    
    # Language verification for Sweden
    print(f"\n🇸🇪 SWEDEN LANGUAGE VERIFICATION")
    print(f"=" * 40)
    
    swedish_chars = 'åäöÅÄÖ'
    english_keywords = ['the', 'and', 'with', 'for', 'quality', 'professional', 'features', 'benefits']
    
    if sweden_listing.amazon_aplus_content:
        has_swedish = any(char in sweden_listing.amazon_aplus_content for char in swedish_chars)
        english_found = [word for word in english_keywords if word.lower() in sweden_listing.amazon_aplus_content.lower()]
        
        print(f"Swedish characters present: {'✅' if has_swedish else '❌'}")
        print(f"English contamination: {'❌ (' + str(len(english_found)) + ' words)' if english_found else '✅'}")
        
        if english_found:
            print(f"English words found: {english_found[:10]}")
    
    # Production readiness assessment
    print(f"\n📈 PRODUCTION READINESS ASSESSMENT")
    print(f"=" * 40)
    
    sweden_ready = (
        sweden_analysis.get('section_count', 0) >= 6 and
        sweden_analysis.get('total_content_length', 0) >= 2000 and
        sweden_listing.quality_score and sweden_listing.quality_score >= 7.0
    )
    
    print(f"Sweden Production Ready: {'✅ YES' if sweden_ready else '❌ NO'}")
    
    if not sweden_ready:
        print(f"\nWhat Sweden needs for 10/10 quality:")
        if sweden_analysis.get('section_count', 0) < 6:
            print(f"  🔧 Increase A+ sections to 8 (currently: {sweden_analysis.get('section_count', 0)})")
        if sweden_analysis.get('total_content_length', 0) < 2000:
            print(f"  🔧 Increase content volume to 3000+ chars (currently: {sweden_analysis.get('total_content_length', 0)})")
        if not sweden_listing.quality_score or sweden_listing.quality_score < 7.0:
            print(f"  🔧 Improve quality score to 8+ (currently: {sweden_listing.quality_score})")
    
    return sweden_analysis, mexico_analysis

if __name__ == "__main__":
    compare_sweden_mexico_aplus()