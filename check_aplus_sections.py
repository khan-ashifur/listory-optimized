import os
import sys
import django

# Set up the backend path correctly
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)
os.chdir(backend_path)

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory.settings')
django.setup()

from apps.listings.models import GeneratedListing

def check_latest_turkey_listing():
    try:
        # Get the latest Turkey listing
        latest_listing = GeneratedListing.objects.filter(
            product__marketplace='tr'
        ).order_by('-created_at').first()
        
        if not latest_listing:
            print("❌ No Turkey listings found")
            return
            
        print(f"📊 Latest Turkey Listing Analysis (ID: {latest_listing.id})")
        print(f"   - Title: {latest_listing.title[:100]}...")
        print(f"   - A+ Content length: {len(latest_listing.amazon_aplus_content) if latest_listing.amazon_aplus_content else 0}")
        
        if latest_listing.amazon_aplus_content:
            aplus_content = latest_listing.amazon_aplus_content
            
            # Count total sections
            total_sections = aplus_content.count('class="aplus-section')
            print(f"   - Total A+ sections: {total_sections}")
            
            # Check for specific sections
            section_indicators = [
                ('Hero', 'hero'),
                ('Features', 'features'),
                ('Usage', 'usage'),
                ('Quality', 'quality'),
                ('Guarantee', 'guarantee'),
                ('Social Proof', 'social'),
                ('Comparison', 'comparison'),
                ('Package', 'package')
            ]
            
            found_sections = []
            for name, indicator in section_indicators:
                if indicator in aplus_content.lower():
                    found_sections.append(name)
                    print(f"   ✅ {name} section detected")
                else:
                    print(f"   ❌ {name} section MISSING")
            
            print(f"\n📈 Section Summary: {len(found_sections)}/8 sections found")
            
            # Show structure of content
            print(f"\n📝 Content Structure Analysis:")
            if 'section1' in aplus_content:
                print("   ✅ Structured section format detected")
            else:
                print("   ❌ No structured section format")
                
            # Check for fallback content
            if 'fallback' in aplus_content.lower():
                print("   ⚠️ Fallback content detected")
            else:
                print("   ✅ No fallback content")
                
        else:
            print("   ❌ NO A+ Content found!")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_latest_turkey_listing()