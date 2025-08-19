#!/usr/bin/env python3
"""
Comprehensive Poland Listing Generation and Quality Analysis
Generates a complete Polish listing and performs line-by-line quality checks
"""

import os
import sys
import django
from datetime import datetime

# Add the backend directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory.settings')
django.setup()

from django.contrib.auth.models import User
from apps.core.models import Product
from apps.listings.models import GeneratedListing
from apps.listings.services import ListingGeneratorService

def create_test_product():
    """Create a test knife sharpener product for Poland market"""
    try:
        # Delete existing test product if it exists
        existing = Product.objects.filter(name__icontains="Polish Kitchen Knife Sharpener").first()
        if existing:
            existing.delete()
            print("🗑️ Deleted existing test product")
        
        # Get or create test user
        user, created = User.objects.get_or_create(
            username='test_user',
            defaults={'email': 'test@example.com'}
        )
        
        product = Product.objects.create(
            user=user,
            name="Polish Kitchen Knife Sharpener - Professional Steel",
            description="Professional knife sharpener for Polish kitchens",
            brand_name="ProSharp",
            price=89.99,
            marketplace='pl',  # Poland marketplace
            marketplace_language='pl',     # Polish language
            occasion='boze_narodzenie',  # Christmas
            brand_tone='luxury',  # Luxury brand tone
            target_platform='amazon'  # Target Amazon platform
        )
        
        print(f"✅ Created test product: {product.name} (ID: {product.id})")
        print(f"   Marketplace: {product.marketplace}")
        print(f"   Language: {product.marketplace_language}")
        print(f"   Occasion: {product.occasion}")
        print(f"   Brand Tone: {product.brand_tone}")
        
        return product
        
    except Exception as e:
        print(f"❌ Error creating test product: {str(e)}")
        return None

def generate_listing(product):
    """Generate a complete Amazon listing for the product"""
    try:
        print(f"\n🔄 Generating listing for product ID: {product.id}")
        
        # Delete existing listings for this product
        existing_listings = GeneratedListing.objects.filter(product=product)
        if existing_listings.exists():
            existing_listings.delete()
            print("🗑️ Deleted existing listings")
        
        # Generate new listing
        service = ListingGeneratorService()
        listing = service.generate_listing(product.id, 'amazon')
        
        print(f"✅ Generated listing (ID: {listing.id})")
        print(f"   Status: {listing.status}")
        
        return listing
        
    except Exception as e:
        print(f"❌ Error generating listing: {str(e)}")
        return None

def analyze_content_quality(listing):
    """Perform comprehensive line-by-line quality analysis"""
    
    print("\n" + "="*80)
    print("🔍 COMPREHENSIVE POLAND LISTING QUALITY ANALYSIS")
    print("="*80)
    
    quality_report = {
        'title': {'status': 'UNKNOWN', 'issues': []},
        'description': {'status': 'UNKNOWN', 'issues': []},
        'bullet_points': {'status': 'UNKNOWN', 'issues': []},
        'faqs': {'status': 'UNKNOWN', 'issues': []},
        'aplus_content': {'status': 'UNKNOWN', 'issues': []},
        'trust_builders': {'status': 'UNKNOWN', 'issues': []},
        'social_proof': {'status': 'UNKNOWN', 'issues': []},
        'overall_score': 0
    }
    
    # Check Title
    print("\n📝 TITLE ANALYSIS:")
    print("-" * 40)
    if hasattr(listing, 'title') and listing.title:
        title = listing.title.strip()
        print(f"Title: {title}")
        print(f"Length: {len(title)} characters")
        
        # Check for English fallbacks
        english_indicators = ['Premium Quality', 'Professional', 'Kitchen', 'Steel', 'Sharpener']
        polish_indicators = ['Profesjonalny', 'Kuchenny', 'Ostrzałka', 'Noże', 'Stalowy']
        
        if len(title) >= 150:
            quality_report['title']['status'] = 'GOOD'
            print("✅ Title length adequate (150+ chars)")
        else:
            quality_report['title']['issues'].append(f"Title too short: {len(title)} chars (need 150+)")
            print(f"❌ Title too short: {len(title)} chars (need 150+)")
        
        # Check for Polish content
        if any(indicator in title for indicator in polish_indicators):
            print("✅ Contains Polish keywords")
        else:
            quality_report['title']['issues'].append("No Polish keywords detected")
            print("❌ No Polish keywords detected")
        
        # Check for English fallbacks
        english_count = sum(1 for indicator in english_indicators if indicator in title)
        if english_count > 0:
            quality_report['title']['issues'].append(f"Contains {english_count} English fallback terms")
            print(f"⚠️ Contains {english_count} English fallback terms")
    else:
        quality_report['title']['status'] = 'FAIL'
        quality_report['title']['issues'].append("Title missing")
        print("❌ Title missing")
    
    # Check Description
    print("\n📄 DESCRIPTION ANALYSIS:")
    print("-" * 40)
    if hasattr(listing, 'long_description') and listing.long_description:
        description = listing.long_description.strip()
        print(f"Description length: {len(description)} characters")
        
        if len(description) >= 1000:
            print("✅ Description length adequate (1000+ chars)")
        else:
            quality_report['description']['issues'].append(f"Description too short: {len(description)} chars")
            print(f"❌ Description too short: {len(description)} chars")
        
        # Check for Polish content
        polish_words = ['kuchenny', 'profesjonalny', 'wysokiej jakości', 'idealny', 'noże']
        polish_count = sum(1 for word in polish_words if word.lower() in description.lower())
        if polish_count >= 3:
            print(f"✅ Contains {polish_count} Polish terms")
        else:
            quality_report['description']['issues'].append(f"Insufficient Polish content: {polish_count} terms")
            print(f"❌ Insufficient Polish content: {polish_count} terms")
            
        # Check for Christmas/occasion content
        christmas_words = ['boże narodzenie', 'święta', 'prezent', 'wigilia']
        christmas_count = sum(1 for word in christmas_words if word.lower() in description.lower())
        if christmas_count > 0:
            print(f"✅ Contains {christmas_count} Christmas-related terms")
        else:
            quality_report['description']['issues'].append("No Christmas occasion keywords")
            print("⚠️ No Christmas occasion keywords")
            
        # Show first 200 chars
        print(f"Preview: {description[:200]}...")
    else:
        quality_report['description']['status'] = 'FAIL'
        quality_report['description']['issues'].append("Description missing")
        print("❌ Description missing")
    
    # Check Bullet Points
    print("\n🔹 BULLET POINTS ANALYSIS:")
    print("-" * 40)
    if hasattr(listing, 'bullet_points') and listing.bullet_points:
        bullet_points = listing.bullet_points.strip()
        bullets = [b.strip() for b in bullet_points.split('\n') if b.strip()]
        print(f"Number of bullet points: {len(bullets)}")
        
        if len(bullets) >= 4:
            print("✅ Adequate number of bullet points (4+)")
        else:
            quality_report['bullet_points']['issues'].append(f"Too few bullet points: {len(bullets)}")
            print(f"❌ Too few bullet points: {len(bullets)}")
        
        # Check each bullet for Polish content
        polish_bullets = 0
        for i, bullet in enumerate(bullets):
            print(f"Bullet {i+1}: {bullet[:100]}...")
            if any(word in bullet.lower() for word in ['profesjonalny', 'wysokiej', 'jakości', 'idealny']):
                polish_bullets += 1
        
        if polish_bullets >= len(bullets) * 0.8:  # 80% should be Polish
            print(f"✅ {polish_bullets}/{len(bullets)} bullets contain Polish content")
        else:
            quality_report['bullet_points']['issues'].append(f"Insufficient Polish bullets: {polish_bullets}/{len(bullets)}")
            print(f"❌ Insufficient Polish bullets: {polish_bullets}/{len(bullets)}")
    else:
        quality_report['bullet_points']['status'] = 'FAIL'
        quality_report['bullet_points']['issues'].append("Bullet points missing")
        print("❌ Bullet points missing")
    
    # Check FAQs
    print("\n❓ FAQ ANALYSIS:")
    print("-" * 40)
    if hasattr(listing, 'faqs') and listing.faqs:
        faqs = listing.faqs.strip()
        print(f"FAQ content length: {len(faqs)} characters")
        
        # Check for Polish P:/O: format
        if 'P:' in faqs and 'O:' in faqs:
            print("✅ Uses Polish P:/O: format")
            
            # Count P:/O: pairs
            p_count = faqs.count('P:')
            o_count = faqs.count('O:')
            print(f"FAQ pairs: {min(p_count, o_count)}")
            
            if min(p_count, o_count) >= 3:
                print("✅ Adequate number of FAQ pairs (3+)")
            else:
                quality_report['faqs']['issues'].append(f"Too few FAQ pairs: {min(p_count, o_count)}")
                print(f"❌ Too few FAQ pairs: {min(p_count, o_count)}")
        else:
            quality_report['faqs']['issues'].append("Missing Polish P:/O: format")
            print("❌ Missing Polish P:/O: format")
        
        # Check for product-specific content
        if 'ostrzałka' in faqs.lower() or 'noże' in faqs.lower():
            print("✅ Contains product-specific terms")
        else:
            quality_report['faqs']['issues'].append("No product-specific FAQ content")
            print("⚠️ No product-specific FAQ content")
            
        # Show first FAQ
        lines = faqs.split('\n')
        if len(lines) >= 2:
            print(f"First FAQ preview:")
            print(f"  {lines[0][:100]}...")
            print(f"  {lines[1][:100]}...")
    else:
        quality_report['faqs']['status'] = 'FAIL'
        quality_report['faqs']['issues'].append("FAQs missing")
        print("❌ FAQs missing")
    
    # Check A+ Content
    print("\n🎨 A+ CONTENT ANALYSIS:")
    print("-" * 40)
    if hasattr(listing, 'amazon_aplus_content') and listing.amazon_aplus_content:
        aplus = listing.amazon_aplus_content.strip()
        print(f"A+ content length: {len(aplus)} characters")
        
        # Count sections
        section_count = aplus.count('<div class="aplus-section"')
        print(f"A+ sections found: {section_count}")
        
        if section_count >= 8:
            print("✅ Adequate A+ sections (8+)")
        else:
            quality_report['aplus_content']['issues'].append(f"Insufficient A+ sections: {section_count}")
            print(f"❌ Insufficient A+ sections: {section_count} (need 8)")
        
        # Check for ENGLISH: image descriptions
        english_desc_count = aplus.count('ENGLISH:')
        print(f"ENGLISH: image descriptions: {english_desc_count}")
        
        if english_desc_count >= section_count:
            print("✅ All sections have ENGLISH: image descriptions")
        else:
            quality_report['aplus_content']['issues'].append(f"Missing ENGLISH: descriptions: {english_desc_count}/{section_count}")
            print(f"❌ Missing ENGLISH: descriptions: {english_desc_count}/{section_count}")
        
        # Check for Polish content in A+
        polish_aplus_indicators = ['profesjonalny', 'wysokiej jakości', 'idealny', 'kuchenny']
        polish_aplus_count = sum(1 for indicator in polish_aplus_indicators if indicator.lower() in aplus.lower())
        if polish_aplus_count >= 5:
            print(f"✅ Rich Polish content in A+: {polish_aplus_count} indicators")
        else:
            quality_report['aplus_content']['issues'].append(f"Limited Polish A+ content: {polish_aplus_count} indicators")
            print(f"⚠️ Limited Polish A+ content: {polish_aplus_count} indicators")
    else:
        quality_report['aplus_content']['status'] = 'FAIL'
        quality_report['aplus_content']['issues'].append("A+ content missing")
        print("❌ A+ content missing")
    
    # Check Trust Builders
    print("\n🛡️ TRUST BUILDERS ANALYSIS:")
    print("-" * 40)
    if hasattr(listing, 'trust_builders') and listing.trust_builders:
        trust = listing.trust_builders.strip()
        print(f"Trust builders length: {len(trust)} characters")
        
        # Check for generic fallbacks
        generic_terms = ['Premium Quality', 'Thousands of satisfied customers', 'Money back guarantee']
        generic_count = sum(1 for term in generic_terms if term in trust)
        
        if generic_count == 0:
            print("✅ No generic English fallbacks")
        else:
            quality_report['trust_builders']['issues'].append(f"Contains {generic_count} generic fallbacks")
            print(f"❌ Contains {generic_count} generic fallbacks")
        
        # Check for Polish trust content
        polish_trust_terms = ['gwarancja', 'jakość', 'zadowoleni klienci', 'bezpieczny']
        polish_trust_count = sum(1 for term in polish_trust_terms if term.lower() in trust.lower())
        if polish_trust_count >= 2:
            print(f"✅ Contains Polish trust content: {polish_trust_count} terms")
        else:
            quality_report['trust_builders']['issues'].append(f"Limited Polish trust content: {polish_trust_count} terms")
            print(f"⚠️ Limited Polish trust content: {polish_trust_count} terms")
    else:
        quality_report['trust_builders']['status'] = 'FAIL'
        quality_report['trust_builders']['issues'].append("Trust builders missing")
        print("❌ Trust builders missing")
    
    # Check Social Proof
    print("\n👥 SOCIAL PROOF ANALYSIS:")
    print("-" * 40)
    if hasattr(listing, 'social_proof') and listing.social_proof:
        social = listing.social_proof.strip()
        if social:
            print(f"Social proof length: {len(social)} characters")
            
            # Check for English fallbacks
            if 'customers love' in social.lower() or 'satisfied customers' in social.lower():
                quality_report['social_proof']['issues'].append("Contains English fallback content")
                print("❌ Contains English fallback content")
            else:
                print("✅ No obvious English fallbacks")
        else:
            print("✅ Social proof empty (acceptable - no fallbacks)")
    else:
        print("✅ Social proof empty (acceptable - no fallbacks)")
    
    # Calculate overall score
    total_issues = sum(len(section['issues']) for section in quality_report.values() if isinstance(section, dict) and 'issues' in section)
    max_possible_score = 10
    quality_report['overall_score'] = max(0, max_possible_score - total_issues)
    
    # Final Summary
    print("\n" + "="*80)
    print("📊 FINAL QUALITY SUMMARY")
    print("="*80)
    
    for section, data in quality_report.items():
        if isinstance(data, dict) and 'issues' in data:
            if not data['issues']:
                print(f"✅ {section.upper()}: PERFECT")
            else:
                print(f"❌ {section.upper()}: {len(data['issues'])} issues")
                for issue in data['issues']:
                    print(f"   - {issue}")
    
    print(f"\n🏆 OVERALL QUALITY SCORE: {quality_report['overall_score']}/10")
    
    if quality_report['overall_score'] >= 8:
        print("🎉 EXCELLENT QUALITY - Matches Mexico standards")
    elif quality_report['overall_score'] >= 6:
        print("👍 GOOD QUALITY - Minor improvements needed")
    elif quality_report['overall_score'] >= 4:
        print("⚠️ FAIR QUALITY - Several issues to fix")
    else:
        print("🚨 POOR QUALITY - Major improvements required")
    
    return quality_report

def save_html_report(listing, quality_report):
    """Save detailed HTML report"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"poland_comprehensive_analysis_{timestamp}.html"
    
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Poland Listing Quality Analysis - {timestamp}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; line-height: 1.6; }}
        .header {{ background: #2c3e50; color: white; padding: 20px; text-align: center; }}
        .section {{ margin: 20px 0; padding: 15px; border: 1px solid #ddd; }}
        .good {{ background: #d4edda; border-color: #c3e6cb; }}
        .warning {{ background: #fff3cd; border-color: #ffeaa7; }}
        .error {{ background: #f8d7da; border-color: #f5c6cb; }}
        .content {{ background: #f8f9fa; padding: 10px; border-left: 4px solid #007bff; }}
        .score {{ font-size: 2em; font-weight: bold; text-align: center; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🇵🇱 Poland Listing Quality Analysis</h1>
        <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <div class="score">Overall Score: {quality_report['overall_score']}/10</div>
    </div>
    
    <div class="section">
        <h2>📝 Title Analysis</h2>
        <div class="content">
            <strong>Title:</strong> {getattr(listing, 'title', 'N/A')}<br>
            <strong>Length:</strong> {len(getattr(listing, 'title', '')) if hasattr(listing, 'title') else 0} characters
        </div>
        {''.join([f"<p style='color: red;'>❌ {issue}</p>" for issue in quality_report['title']['issues']])}
    </div>
    
    <div class="section">
        <h2>📄 Description Analysis</h2>
        <div class="content">
            <strong>Length:</strong> {len(getattr(listing, 'long_description', '')) if hasattr(listing, 'long_description') else 0} characters<br>
            <strong>Preview:</strong> {getattr(listing, 'long_description', 'N/A')[:300] + '...' if hasattr(listing, 'long_description') and len(getattr(listing, 'long_description', '')) > 300 else getattr(listing, 'long_description', 'N/A')}
        </div>
        {''.join([f"<p style='color: red;'>❌ {issue}</p>" for issue in quality_report['description']['issues']])}
    </div>
    
    <div class="section">
        <h2>🔹 Bullet Points Analysis</h2>
        <div class="content">
            {getattr(listing, 'bullet_points', 'N/A').replace(chr(10), '<br>') if hasattr(listing, 'bullet_points') else 'N/A'}
        </div>
        {''.join([f"<p style='color: red;'>❌ {issue}</p>" for issue in quality_report['bullet_points']['issues']])}
    </div>
    
    <div class="section">
        <h2>❓ FAQ Analysis</h2>
        <div class="content">
            {getattr(listing, 'faqs', 'N/A').replace(chr(10), '<br>') if hasattr(listing, 'faqs') else 'N/A'}
        </div>
        {''.join([f"<p style='color: red;'>❌ {issue}</p>" for issue in quality_report['faqs']['issues']])}
    </div>
    
    <div class="section">
        <h2>🎨 A+ Content Analysis</h2>
        <div class="content">
            {getattr(listing, 'amazon_aplus_content', 'N/A')[:1000] + '...' if hasattr(listing, 'amazon_aplus_content') and len(getattr(listing, 'amazon_aplus_content', '')) > 1000 else getattr(listing, 'amazon_aplus_content', 'N/A')}
        </div>
        {''.join([f"<p style='color: red;'>❌ {issue}</p>" for issue in quality_report['aplus_content']['issues']])}
    </div>
    
    <div class="section">
        <h2>📊 Quality Summary</h2>
        <ul>
            {''.join([f"<li>{'✅' if not quality_report[section]['issues'] else '❌'} {section.upper()}: {'PERFECT' if not quality_report[section]['issues'] else f'{len(quality_report[section]['issues'])} issues'}</li>" for section in quality_report if isinstance(quality_report[section], dict) and 'issues' in quality_report[section]])}
        </ul>
    </div>
</body>
</html>
"""
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"\n💾 Saved detailed report: {filename}")
    return filename

def main():
    """Main execution function"""
    print("🇵🇱 Poland Listing Generation and Quality Analysis")
    print("=" * 60)
    
    # Create test product
    product = create_test_product()
    if not product:
        return
    
    # Generate listing
    listing = generate_listing(product)
    if not listing:
        return
    
    # Perform quality analysis
    quality_report = analyze_content_quality(listing)
    
    # Save HTML report
    html_file = save_html_report(listing, quality_report)
    
    print(f"\n🎯 Analysis complete!")
    print(f"📄 HTML Report: {html_file}")
    print(f"🏆 Final Score: {quality_report['overall_score']}/10")

if __name__ == "__main__":
    main()