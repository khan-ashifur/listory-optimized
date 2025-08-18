"""
Simple Turkey A+ Content Test
Just generate a Turkey listing and analyze the A+ content structure
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

def simple_turkey_test():
    """Simple test of Turkey A+ content generation"""
    print("\n" + "="*80)
    print("🇹🇷 TURKEY A+ CONTENT SIMPLE TEST")
    print("="*80)
    
    # Find Turkey product
    turkey_product = Product.objects.filter(marketplace='tr').first()
    if not turkey_product:
        print("❌ No Turkey product found")
        return
    
    print(f"✅ Turkey Product: {turkey_product.name} (ID: {turkey_product.id})")
    
    # Generate listing
    service = ListingGeneratorService()
    
    try:
        print("\n🤖 Generating Turkey listing...")
        listing = service.generate_listing(turkey_product.id, platform='amazon')
        
        print("\n📊 LISTING ANALYSIS:")
        print(f"   Title: {len(listing.title)} chars")
        print(f"   Bullets: {len(listing.bullet_points.split('\\n'))} items")
        
        # Focus on A+ content analysis
        if listing.amazon_aplus_content:
            aplus = listing.amazon_aplus_content
            print(f"\n🎨 A+ CONTENT ANALYSIS:")
            print(f"   Total length: {len(aplus)} characters")
            
            # Count actual sections
            sections = aplus.count('aplus-section-card')
            print(f"   A+ sections: {sections}")
            
            # Check for English image descriptions
            english_count = aplus.count('ENGLISH:')
            print(f"   English image descriptions: {english_count}")
            
            # Check for 8-section structure
            section_names = []
            for i in range(1, 9):
                if f'section{i}_' in aplus:
                    section_names.append(f'section{i}')
            
            print(f"   8-section structure: {len(section_names)}/8")
            if section_names:
                print(f"   Found sections: {section_names}")
            
            # Look for specific keywords that indicate comprehensive content
            quality_indicators = [
                ('Turkish content', any(word in aplus for word in ['kalite', 'garanti', 'Türkiye'])),
                ('Family focus', 'aile' in aplus),
                ('Trust elements', any(word in aplus for word in ['güven', 'sertifika', 'orijinal'])),
                ('Professional structure', 'keywords' in aplus and 'imageDescription' in aplus),
                ('Complete sections', sections >= 6)
            ]
            
            print(f"\\n✅ QUALITY INDICATORS:")
            score = 0
            for indicator, passed in quality_indicators:
                status = "✅" if passed else "❌"
                print(f"   {status} {indicator}")
                if passed:
                    score += 20
            
            print(f"\\n🎯 TURKEY A+ QUALITY SCORE: {score}/100")
            
            if score >= 80:
                print("✅ EXCELLENT - Matches Mexico quality!")
                print("✅ Ready to beat Helium 10, Jasper AI, CopyMonkey")
            elif score >= 60:
                print("⚠️ GOOD - Needs minor improvements")
            else:
                print("❌ NEEDS IMPROVEMENT - Major fixes required")
                
                # Specific recommendations
                print("\\n🔧 RECOMMENDATIONS:")
                if sections < 8:
                    print("   1. Ensure 8 A+ content sections are generated")
                if english_count < 6:
                    print("   2. Add English image descriptions to all sections")
                if 'ENGLISH:' not in aplus:
                    print("   3. Add 'ENGLISH:' prefix to imageDescription fields")
            
            # Save sample for manual review
            sample_file = f"turkey_aplus_sample.html"
            with open(sample_file, 'w', encoding='utf-8') as f:
                f.write(f"""
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>Turkey A+ Content Sample</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-50 p-8">
    <div class="max-w-6xl mx-auto">
        <h1 class="text-3xl font-bold mb-6">🇹🇷 Turkey A+ Content Analysis</h1>
        
        <div class="bg-white p-6 rounded-lg shadow mb-6">
            <h2 class="text-xl font-bold mb-4">Quality Metrics</h2>
            <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div class="bg-gray-50 p-3 rounded">
                    <div class="text-sm text-gray-600">A+ Sections</div>
                    <div class="text-2xl font-bold">{sections}</div>
                </div>
                <div class="bg-gray-50 p-3 rounded">
                    <div class="text-sm text-gray-600">English Images</div>
                    <div class="text-2xl font-bold">{english_count}</div>
                </div>
                <div class="bg-gray-50 p-3 rounded">
                    <div class="text-sm text-gray-600">Quality Score</div>
                    <div class="text-2xl font-bold">{score}/100</div>
                </div>
                <div class="bg-gray-50 p-3 rounded">
                    <div class="text-sm text-gray-600">Content Length</div>
                    <div class="text-2xl font-bold">{len(aplus)}</div>
                </div>
            </div>
        </div>
        
        <div class="bg-white p-6 rounded-lg shadow">
            <h2 class="text-xl font-bold mb-4">A+ Content</h2>
            <div class="border rounded p-4">
                {aplus}
            </div>
        </div>
    </div>
</body>
</html>
                """)
            
            print(f"\\n📄 Sample saved to: {sample_file}")
            
        else:
            print("\\n❌ No A+ content generated!")
            print("🔧 This indicates a serious issue with the Turkey implementation")
        
        return listing
        
    except Exception as e:
        print(f"\\n❌ Error generating Turkey listing: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    simple_turkey_test()