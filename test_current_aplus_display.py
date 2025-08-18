"""
Test what A+ content is currently being displayed in the interface
"""

import os
import sys
import django

# Add the project path and configure Django
project_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.append(project_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory.settings')
django.setup()

def test_current_aplus_display():
    """Test what A+ content is currently being displayed"""
    
    try:
        from apps.listings.models import GeneratedListing
        from django.contrib.auth.models import User
        
        print("🔍 CHECKING CURRENT A+ CONTENT IN DATABASE")
        print("=" * 60)
        
        # Get the most recent listing
        recent_listings = GeneratedListing.objects.all().order_by('-created_at')[:5]
        
        if not recent_listings:
            print("❌ No listings found in database")
            return False
        
        print(f"📊 Found {len(recent_listings)} recent listings:")
        
        for i, listing in enumerate(recent_listings, 1):
            print(f"\n📄 LISTING {i} (ID: {listing.id}):")
            print(f"   Created: {listing.created_at}")
            print(f"   Title: {listing.title[:60]}...")
            
            aplus_content = listing.amazon_aplus_content or ""
            print(f"   A+ Content Length: {len(aplus_content):,} characters")
            
            if aplus_content:
                # Check if it's HTML sections or plain content
                has_sections = '<h3>' in aplus_content and '</h3>' in aplus_content
                has_html_template = '<div class="aplus-introduction' in aplus_content
                
                print(f"   Has sections: {'✅' if has_sections else '❌'}")
                print(f"   Is HTML template: {'⚠️' if has_html_template else '✅ Clean'}")
                
                if has_sections and not has_html_template:
                    sections = aplus_content.split('<h3>')[1:]
                    print(f"   Sections count: {len(sections)}")
                    
                    # Show first few sections
                    for j, section in enumerate(sections[:3], 1):
                        if '</h3>' in section:
                            title = section.split('</h3>')[0]
                            print(f"      Section {j}: {title}")
                
                # Show a preview of the content
                preview = aplus_content[:200].replace('\n', ' ')
                print(f"   Content preview: {preview}...")
            else:
                print("   ❌ No A+ content")
        
        # Show the most recent one in detail
        if recent_listings:
            latest = recent_listings[0]
            aplus_content = latest.amazon_aplus_content or ""
            
            print(f"\n📋 LATEST LISTING A+ CONTENT DETAIL:")
            print(f"   Full content ({len(aplus_content)} chars):")
            print("   " + "="*50)
            print(aplus_content[:1000] + ("..." if len(aplus_content) > 1000 else ""))
            print("   " + "="*50)
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_current_aplus_display()