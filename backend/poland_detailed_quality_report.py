#!/usr/bin/env python3
"""
Detailed Poland Listing Quality Report
Creates comprehensive line-by-line analysis with actual content examination
"""

import os
import sys
import django
from datetime import datetime
import re

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory.settings')
django.setup()

from apps.listings.models import GeneratedListing

def analyze_poland_listing():
    """Comprehensive analysis of the Poland listing"""
    
    # Get the latest listing
    listing = GeneratedListing.objects.latest('created_at')
    
    print("🇵🇱 POLAND LISTING COMPREHENSIVE QUALITY ANALYSIS")
    print("=" * 80)
    print(f"Listing ID: {listing.id}")
    print(f"Generated: {listing.created_at}")
    print(f"Product: {listing.product.name}")
    print(f"Marketplace: {listing.product.marketplace}")
    print(f"Language: {listing.product.marketplace_language}")
    print(f"Occasion: {listing.product.occasion}")
    print(f"Brand Tone: {listing.product.brand_tone}")
    print()
    
    quality_issues = []
    quality_score = 0
    max_score = 100
    
    # 1. TITLE ANALYSIS (20 points)
    print("📝 TITLE ANALYSIS (20 points)")
    print("-" * 50)
    
    title = listing.title.strip() if listing.title else ""
    print(f"Title: {title}")
    print(f"Length: {len(title)} characters")
    
    title_score = 0
    
    # Length check (5 points)
    if len(title) >= 150:
        title_score += 5
        print("✅ Length adequate (150+ chars) - 5/5 points")
    else:
        print(f"❌ Title too short: {len(title)} chars (need 150+) - 0/5 points")
        quality_issues.append(f"Title too short: {len(title)} characters")
    
    # Polish content check (10 points)
    polish_title_terms = ['ostrzałka', 'noży', 'kuchennych', 'profesjonalna', 'stalowa', 'jakości']
    polish_count = sum(1 for term in polish_title_terms if term.lower() in title.lower())
    polish_score = min(10, polish_count * 2)
    title_score += polish_score
    print(f"✅ Polish content: {polish_count}/6 terms found - {polish_score}/10 points")
    
    # Christmas occasion check (5 points)
    christmas_terms = ['boże narodzenie', 'prezent', 'świąteczny', 'wigilia']
    christmas_count = sum(1 for term in christmas_terms if term.lower() in title.lower())
    if christmas_count > 0:
        title_score += 5
        print(f"✅ Christmas occasion: {christmas_count} terms - 5/5 points")
    else:
        print("❌ No Christmas occasion terms - 0/5 points")
        quality_issues.append("Title missing Christmas occasion keywords")
    
    print(f"📊 Title Score: {title_score}/20 points")
    quality_score += title_score
    print()
    
    # 2. DESCRIPTION ANALYSIS (25 points)
    print("📄 DESCRIPTION ANALYSIS (25 points)")
    print("-" * 50)
    
    description = listing.long_description.strip() if listing.long_description else ""
    print(f"Description length: {len(description)} characters")
    print(f"Preview: {description[:200]}...")
    
    desc_score = 0
    
    # Length check (5 points)
    if len(description) >= 1000:
        desc_score += 5
        print("✅ Length adequate (1000+ chars) - 5/5 points")
    else:
        print(f"❌ Description too short: {len(description)} chars - 0/5 points")
        quality_issues.append(f"Description too short: {len(description)} characters")
    
    # Polish content richness (15 points)
    polish_desc_terms = [
        'solidna', 'stalowa', 'prosharp', 'polskich', 'rodzin', 'jakość', 
        'bezpieczeństwo', 'kuchni', 'profesjonalnej', 'skuteczne', 'wytrzymała',
        'ergonomiczna', 'antypoślizgowa', 'precyzyjne'
    ]
    polish_desc_count = sum(1 for term in polish_desc_terms if term.lower() in description.lower())
    polish_desc_score = min(15, polish_desc_count)
    desc_score += polish_desc_score
    print(f"✅ Polish richness: {polish_desc_count}/14+ terms - {polish_desc_score}/15 points")
    
    # Christmas/occasion content (5 points)
    christmas_desc_count = sum(1 for term in christmas_terms if term.lower() in description.lower())
    if christmas_desc_count > 0:
        desc_score += 5
        print(f"✅ Christmas content: {christmas_desc_count} terms - 5/5 points")
    else:
        print("❌ No Christmas content in description - 0/5 points")
        quality_issues.append("Description missing Christmas occasion content")
    
    print(f"📊 Description Score: {desc_score}/25 points")
    quality_score += desc_score
    print()
    
    # 3. BULLET POINTS ANALYSIS (20 points)
    print("🔹 BULLET POINTS ANALYSIS (20 points)")
    print("-" * 50)
    
    bullets = listing.bullet_points.strip() if listing.bullet_points else ""
    bullet_list = [b.strip() for b in bullets.split('\n') if b.strip()] if bullets else []
    
    print(f"Number of bullet points: {len(bullet_list)}")
    
    bullet_score = 0
    
    # Count check (5 points)
    if len(bullet_list) >= 4:
        bullet_score += 5
        print("✅ Adequate count (4+) - 5/5 points")
    else:
        print(f"❌ Too few bullets: {len(bullet_list)} - 0/5 points")
        quality_issues.append(f"Insufficient bullet points: {len(bullet_list)}")
    
    # Polish content in bullets (10 points)
    polish_bullet_count = 0
    for i, bullet in enumerate(bullet_list):
        print(f"Bullet {i+1}: {bullet[:80]}...")
        if any(term in bullet.lower() for term in ['profesjonalna', 'wytrzymały', 'bezpieczne', 'jakość', 'elegancki']):
            polish_bullet_count += 1
    
    if polish_bullet_count >= len(bullet_list) * 0.8:  # 80% should be Polish
        bullet_score += 10
        print(f"✅ Polish content: {polish_bullet_count}/{len(bullet_list)} bullets - 10/10 points")
    else:
        bullet_score += polish_bullet_count * 2
        print(f"⚠️ Polish content: {polish_bullet_count}/{len(bullet_list)} bullets - {polish_bullet_count * 2}/10 points")
        quality_issues.append(f"Limited Polish content in bullets: {polish_bullet_count}/{len(bullet_list)}")
    
    # Conversion focus (5 points)
    conversion_terms = ['idealna', 'doskonały', 'prezent', 'łatwe', 'szybkie', 'bezpieczne']
    conversion_bullet_count = sum(1 for bullet in bullet_list for term in conversion_terms if term.lower() in bullet.lower())
    if conversion_bullet_count >= 3:
        bullet_score += 5
        print("✅ Conversion-focused content - 5/5 points")
    else:
        bullet_score += conversion_bullet_count
        print(f"⚠️ Limited conversion focus - {conversion_bullet_count}/5 points")
    
    print(f"📊 Bullet Points Score: {bullet_score}/20 points")
    quality_score += bullet_score
    print()
    
    # 4. A+ CONTENT ANALYSIS (20 points)
    print("🎨 A+ CONTENT ANALYSIS (20 points)")
    print("-" * 50)
    
    aplus = listing.amazon_aplus_content.strip() if listing.amazon_aplus_content else ""
    print(f"A+ content length: {len(aplus)} characters")
    
    aplus_score = 0
    
    # Content existence (5 points)
    if len(aplus) >= 10000:
        aplus_score += 5
        print("✅ Rich A+ content (10k+ chars) - 5/5 points")
    else:
        print(f"❌ Limited A+ content: {len(aplus)} chars - 0/5 points")
        quality_issues.append(f"Insufficient A+ content: {len(aplus)} characters")
    
    # ENGLISH image descriptions (10 points)
    english_count = aplus.count('ENGLISH:')
    print(f"ENGLISH: image descriptions found: {english_count}")
    if english_count >= 6:
        aplus_score += 10
        print("✅ Comprehensive image descriptions - 10/10 points")
    else:
        aplus_score += english_count
        print(f"⚠️ Limited image descriptions - {english_count}/10 points")
        quality_issues.append(f"Missing ENGLISH: descriptions: {english_count}/6+")
    
    # Polish content in A+ (5 points)
    polish_aplus_terms = ['profesjonalny', 'wysokiej jakości', 'elegancki', 'wytrzymały', 'bezpieczny']
    polish_aplus_count = sum(1 for term in polish_aplus_terms if term.lower() in aplus.lower())
    aplus_polish_score = min(5, polish_aplus_count)
    aplus_score += aplus_polish_score
    print(f"✅ Polish A+ content: {polish_aplus_count} terms - {aplus_polish_score}/5 points")
    
    print(f"📊 A+ Content Score: {aplus_score}/20 points")
    quality_score += aplus_score
    print()
    
    # 5. TRUST BUILDERS ANALYSIS (10 points)
    print("🛡️ TRUST BUILDERS ANALYSIS (10 points)")
    print("-" * 50)
    
    trust = listing.trust_builders.strip() if listing.trust_builders else ""
    print(f"Trust builders: {trust}")
    
    trust_score = 0
    
    # Content check (5 points)
    if len(trust) >= 100:
        trust_score += 5
        print("✅ Adequate trust content - 5/5 points")
    else:
        print(f"❌ Limited trust content: {len(trust)} chars - 0/5 points")
        quality_issues.append("Insufficient trust builders content")
    
    # Polish trust elements (5 points)
    polish_trust_terms = ['gwarancji', 'certyfikat', 'serwisem', 'polsce', 'bezpieczeństwo', 'jakość']
    polish_trust_count = sum(1 for term in polish_trust_terms if term.lower() in trust.lower())
    trust_polish_score = min(5, polish_trust_count)
    trust_score += trust_polish_score
    print(f"✅ Polish trust elements: {polish_trust_count} terms - {trust_polish_score}/5 points")
    
    print(f"📊 Trust Builders Score: {trust_score}/10 points")
    quality_score += trust_score
    print()
    
    # 6. FAQ ANALYSIS (5 points)
    print("❓ FAQ ANALYSIS (5 points)")
    print("-" * 50)
    
    faqs = listing.faqs.strip() if listing.faqs else ""
    
    faq_score = 0
    
    if not faqs:
        print("❌ FAQs completely missing - 0/5 points")
        quality_issues.append("FAQs missing entirely")
    else:
        print(f"FAQ content length: {len(faqs)} characters")
        if 'P:' in faqs and 'O:' in faqs:
            p_count = faqs.count('P:')
            o_count = faqs.count('O:')
            faq_pairs = min(p_count, o_count)
            print(f"Polish P:/O: format with {faq_pairs} pairs")
            faq_score = min(5, faq_pairs)
            print(f"✅ FAQ structure - {faq_score}/5 points")
        else:
            print("❌ Missing Polish P:/O: format - 0/5 points")
            quality_issues.append("FAQs missing Polish P:/O: format")
    
    print(f"📊 FAQ Score: {faq_score}/5 points")
    quality_score += faq_score
    print()
    
    # FINAL QUALITY ASSESSMENT
    print("=" * 80)
    print("📊 FINAL QUALITY ASSESSMENT")
    print("=" * 80)
    
    print(f"🏆 TOTAL SCORE: {quality_score}/{max_score} points ({quality_score/max_score*100:.1f}%)")
    
    if quality_score >= 80:
        grade = "A (EXCELLENT)"
        status = "🎉 Matches Mexico quality standards"
    elif quality_score >= 70:
        grade = "B (GOOD)"
        status = "👍 Good quality, minor improvements needed"
    elif quality_score >= 60:
        grade = "C (FAIR)"
        status = "⚠️ Fair quality, several improvements needed"
    elif quality_score >= 50:
        grade = "D (POOR)"
        status = "🚨 Poor quality, major improvements required"
    else:
        grade = "F (FAILING)"
        status = "💥 Failing quality, complete revision needed"
    
    print(f"📈 GRADE: {grade}")
    print(f"📋 STATUS: {status}")
    print()
    
    # Issue Summary
    if quality_issues:
        print("🚨 QUALITY ISSUES IDENTIFIED:")
        for i, issue in enumerate(quality_issues, 1):
            print(f"   {i}. {issue}")
    else:
        print("✅ NO QUALITY ISSUES FOUND!")
    
    print()
    
    # Comparison with Mexico Standards
    print("🔍 COMPARISON WITH MEXICO STANDARDS:")
    print("-" * 40)
    
    mexico_standards = {
        "Title": "150+ chars, rich Polish content, occasion keywords",
        "Description": "1000+ chars, compelling Polish narrative, Christmas focus", 
        "Bullets": "4+ conversion-focused bullets with Polish content",
        "A+ Content": "8+ sections with detailed ENGLISH: image descriptions",
        "FAQs": "Polish P:/O: format with product-specific questions",
        "Trust": "Polish-specific trust elements, no generic fallbacks"
    }
    
    for category, standard in mexico_standards.items():
        print(f"• {category}: {standard}")
    
    print()
    print("🎯 RECOMMENDATIONS FOR IMPROVEMENT:")
    print("-" * 40)
    
    if quality_score < 80:
        recommendations = []
        
        if len(listing.title) < 150:
            recommendations.append("Extend title to 150+ characters with more Polish keywords")
        
        if not faqs:
            recommendations.append("Add comprehensive FAQs in Polish P:/O: format")
        
        if aplus_score < 15:
            recommendations.append("Enhance A+ content with 8+ structured sections")
        
        if desc_score < 20:
            recommendations.append("Enrich description with more Polish product-specific content")
        
        if bullet_score < 15:
            recommendations.append("Improve bullet points with stronger conversion focus")
        
        for i, rec in enumerate(recommendations, 1):
            print(f"   {i}. {rec}")
    else:
        print("   ✅ Content meets high quality standards!")
    
    return {
        'total_score': quality_score,
        'max_score': max_score,
        'percentage': quality_score/max_score*100,
        'grade': grade,
        'issues': quality_issues,
        'listing_id': listing.id
    }

def save_detailed_html_report(result):
    """Save comprehensive HTML report"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"poland_final_quality_analysis_{timestamp}.html"
    
    # Get the listing again for full content
    listing = GeneratedListing.objects.latest('created_at')
    
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Poland Final Quality Analysis - {timestamp}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; line-height: 1.6; background: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 10px; }}
        .header {{ background: linear-gradient(135deg, #dc143c, #b71c1c); color: white; padding: 30px; text-align: center; border-radius: 10px; margin-bottom: 30px; }}
        .score {{ font-size: 3em; font-weight: bold; margin: 20px 0; }}
        .grade {{ font-size: 1.5em; background: rgba(255,255,255,0.2); padding: 10px 20px; border-radius: 25px; display: inline-block; }}
        .section {{ margin: 30px 0; padding: 20px; border: 2px solid #ddd; border-radius: 10px; }}
        .excellent {{ border-color: #4caf50; background: #f1f8e9; }}
        .good {{ border-color: #2196f3; background: #e3f2fd; }}
        .warning {{ border-color: #ff9800; background: #fff3e0; }}
        .error {{ border-color: #f44336; background: #ffebee; }}
        .content-box {{ background: #f8f9fa; padding: 15px; border-radius: 5px; margin: 10px 0; border-left: 4px solid #007bff; }}
        .issue {{ color: #d32f2f; margin: 5px 0; }}
        .success {{ color: #388e3c; margin: 5px 0; }}
        h2 {{ color: #1976d2; border-bottom: 2px solid #1976d2; padding-bottom: 10px; }}
        h3 {{ color: #424242; }}
        .flag {{ font-size: 2em; }}
        .metrics {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 20px 0; }}
        .metric {{ background: white; padding: 15px; border-radius: 10px; text-align: center; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="flag">🇵🇱</div>
            <h1>Poland Listing Final Quality Analysis</h1>
            <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <div class="score">{result['total_score']}/{result['max_score']}</div>
            <div class="grade">{result['grade']}</div>
        </div>
        
        <div class="metrics">
            <div class="metric">
                <h3>Overall Score</h3>
                <div style="font-size: 2em; font-weight: bold; color: {'#4caf50' if result['percentage'] >= 80 else '#ff9800' if result['percentage'] >= 60 else '#f44336'}">{result['percentage']:.1f}%</div>
            </div>
            <div class="metric">
                <h3>Listing ID</h3>
                <div style="font-size: 1.5em;">{result['listing_id']}</div>
            </div>
            <div class="metric">
                <h3>Market</h3>
                <div style="font-size: 1.5em;">Poland (pl)</div>
            </div>
            <div class="metric">
                <h3>Occasion</h3>
                <div style="font-size: 1.2em;">Boże Narodzenie</div>
            </div>
        </div>
        
        <div class="section {'excellent' if len(listing.title) >= 150 else 'warning'}">
            <h2>📝 Title Analysis</h2>
            <div class="content-box">
                <strong>Title:</strong> {listing.title}<br>
                <strong>Length:</strong> {len(listing.title)} characters
            </div>
            {'<div class="success">✅ Title length adequate</div>' if len(listing.title) >= 150 else '<div class="issue">❌ Title too short (need 150+ chars)</div>'}
            {'<div class="success">✅ Contains Christmas occasion keywords</div>' if any(term in listing.title.lower() for term in ['boże narodzenie', 'prezent', 'święta']) else '<div class="issue">❌ Missing Christmas keywords</div>'}
        </div>
        
        <div class="section {'excellent' if len(listing.long_description) >= 1000 else 'warning'}">
            <h2>📄 Description Analysis</h2>
            <div class="content-box">
                <strong>Length:</strong> {len(listing.long_description)} characters<br>
                <strong>Content:</strong> {listing.long_description[:500]}{'...' if len(listing.long_description) > 500 else ''}
            </div>
            {'<div class="success">✅ Description length adequate</div>' if len(listing.long_description) >= 1000 else '<div class="issue">❌ Description too short</div>'}
        </div>
        
        <div class="section">
            <h2>🔹 Bullet Points Analysis</h2>
            <div class="content-box">
                {listing.bullet_points.replace(chr(10), '<br>') if listing.bullet_points else 'No bullet points found'}
            </div>
        </div>
        
        <div class="section">
            <h2>🛡️ Trust Builders</h2>
            <div class="content-box">
                {listing.trust_builders if listing.trust_builders else 'No trust builders found'}
            </div>
        </div>
        
        <div class="section {'error' if not listing.faqs else 'good'}">
            <h2>❓ FAQ Analysis</h2>
            <div class="content-box">
                {listing.faqs if listing.faqs else '<div class="issue">❌ FAQs are completely missing</div>'}
            </div>
        </div>
        
        <div class="section">
            <h2>🎨 A+ Content Preview</h2>
            <div class="content-box">
                <strong>Length:</strong> {len(listing.amazon_aplus_content)} characters<br>
                <strong>ENGLISH: descriptions found:</strong> {listing.amazon_aplus_content.count('ENGLISH:')}<br>
                <div style="max-height: 300px; overflow-y: auto; margin-top: 10px;">
                    {listing.amazon_aplus_content[:2000]}{'...' if len(listing.amazon_aplus_content) > 2000 else ''}
                </div>
            </div>
        </div>
        
        <div class="section">
            <h2>🚨 Quality Issues Summary</h2>
            {'<br>'.join([f'<div class="issue">• {issue}</div>' for issue in result["issues"]]) if result["issues"] else '<div class="success">✅ No critical quality issues found!</div>'}
        </div>
        
        <div class="section">
            <h2>🎯 Mexico Standards Comparison</h2>
            <p>This analysis compares the Poland listing against Mexico's high-quality standards:</p>
            <ul>
                <li><strong>Title:</strong> {'✅' if len(listing.title) >= 150 else '❌'} 150+ characters with Polish keywords</li>
                <li><strong>Description:</strong> {'✅' if len(listing.long_description) >= 1000 else '❌'} 1000+ characters compelling narrative</li>
                <li><strong>A+ Content:</strong> {'✅' if listing.amazon_aplus_content.count('ENGLISH:') >= 6 else '❌'} Detailed ENGLISH: image descriptions</li>
                <li><strong>FAQs:</strong> {'✅' if listing.faqs and 'P:' in listing.faqs else '❌'} Polish P:/O: format</li>
                <li><strong>Trust:</strong> {'✅' if 'gwarancji' in listing.trust_builders.lower() or 'certyfikat' in listing.trust_builders.lower() else '❌'} Polish-specific trust elements</li>
            </ul>
        </div>
    </div>
</body>
</html>
"""
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"\n💾 Comprehensive HTML report saved: {filename}")
    return filename

def main():
    """Main execution"""
    print("Starting comprehensive Poland listing quality analysis...")
    result = analyze_poland_listing()
    html_file = save_detailed_html_report(result)
    
    print(f"\n🎯 ANALYSIS COMPLETE!")
    print(f"📊 Final Score: {result['total_score']}/{result['max_score']} ({result['percentage']:.1f}%)")
    print(f"📈 Grade: {result['grade']}")
    print(f"📄 Detailed Report: {html_file}")

if __name__ == "__main__":
    main()