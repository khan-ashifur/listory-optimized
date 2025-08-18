"""
Examine Turkey Listing Line by Line
"""
import os
import sys
import django

# Set up Django
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)
os.chdir(backend_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory.settings')
django.setup()

from apps.listings.models import GeneratedListing

def examine_listing_line_by_line():
    """Examine the latest Turkey listing line by line"""
    try:
        print("🔍 EXAMINING TURKEY LISTING LINE BY LINE")
        print("=" * 60)
        
        # Get the latest listing (ID 977 - with improved lifestyle images)
        listing = GeneratedListing.objects.get(id=977)
        
        print(f"📊 LISTING OVERVIEW:")
        print(f"   - ID: {listing.id}")
        print(f"   - Title: {listing.title}")
        print(f"   - Status: {listing.status}")
        print(f"   - A+ Content Length: {len(listing.amazon_aplus_content)} characters")
        print(f"   - Created: {listing.created_at}")
        
        print(f"\n🎯 A+ CONTENT ANALYSIS:")
        print("=" * 60)
        
        aplus_content = listing.amazon_aplus_content
        
        if not aplus_content:
            print("❌ No A+ content found!")
            return
            
        # Split into lines and analyze
        lines = aplus_content.split('\n')
        print(f"📏 Total lines: {len(lines)}")
        
        # Look for section indicators
        section_count = 0
        div_count = 0
        content_lines = 0
        
        print(f"\n📋 LINE BY LINE ANALYSIS:")
        print("-" * 60)
        
        for i, line in enumerate(lines[:50], 1):  # First 50 lines
            line_stripped = line.strip()
            
            if not line_stripped:
                continue
                
            content_lines += 1
            
            # Check for important markers
            markers = []
            
            if 'aplus-section' in line_stripped:
                section_count += 1
                markers.append(f"SECTION #{section_count}")
                
            if '<div' in line_stripped:
                div_count += 1
                markers.append("DIV")
                
            if any(turkish_word in line_stripped.lower() for turkish_word in ['sensei', 'premium', 'kalite', 'garanti', 'türk']):
                markers.append("TURKISH CONTENT")
                
            if 'imageDescription' in line_stripped:
                markers.append("IMAGE DESC")
                
            if 'Keywords' in line_stripped:
                markers.append("KEYWORDS")
                
            marker_str = " | ".join(markers) if markers else ""
            
            print(f"Line {i:2d}: {line_stripped[:80]:<80} {marker_str}")
            
            if content_lines >= 30:  # Limit output
                break
                
        print("-" * 60)
        
        print(f"\n📈 CONTENT STATISTICS:")
        print(f"   - Total A+ sections found: {section_count}")
        print(f"   - Total div elements: {div_count}")
        print(f"   - Content lines: {content_lines}")
        
        # Check for specific Turkey content
        print(f"\n🇹🇷 TURKEY-SPECIFIC CONTENT CHECK:")
        
        turkey_indicators = [
            ('Sensei', aplus_content.count('Sensei')),
            ('Premium Kalite', aplus_content.count('Premium Kalite')),
            ('Türk', aplus_content.count('Türk')),
            ('Garanti', aplus_content.count('Garanti')),
            ('ENGLISH:', aplus_content.count('ENGLISH:')),
            ('Turkish', aplus_content.count('Turkish')),
        ]
        
        for indicator, count in turkey_indicators:
            print(f"   - '{indicator}': {count} occurrences")
            
        # Look for the 8 sections we expect
        print(f"\n🎯 EXPECTED 8-SECTION STRUCTURE CHECK:")
        expected_sections = [
            'section1_hero', 'section2_features', 'section3_usage', 'section4_quality',
            'section5_social_proof', 'section6_comparison', 'section7_warranty', 'section8_package'
        ]
        
        found_sections = []
        for section in expected_sections:
            if section in aplus_content:
                found_sections.append(section)
                print(f"   ✅ {section}: Found")
            else:
                print(f"   ❌ {section}: Missing")
                
        print(f"\n📊 FINAL SUMMARY:")
        print(f"   - Expected sections: 8")
        print(f"   - Found sections: {len(found_sections)}")
        print(f"   - HTML sections: {section_count}")
        print(f"   - Content quality: {'COMPREHENSIVE' if len(found_sections) >= 6 else 'BASIC'}")
        
        if len(found_sections) < 8:
            print(f"\n🔧 ISSUE IDENTIFIED:")
            print(f"   - Missing {8 - len(found_sections)} sections")
            print(f"   - This explains why content is only {len(aplus_content)} chars instead of 25,000+")
            
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    examine_listing_line_by_line()