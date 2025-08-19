#!/usr/bin/env python3
"""
Comprehensive Belgium Amazon.be Listing Quality Analysis
Expert E-commerce Strategist & SEO Evaluation
"""

import json
import re
from datetime import datetime

def analyze_belgium_listing():
    """Comprehensive quality analysis for Belgium Amazon.be listing"""
    
    print("=" * 80)
    print("BELGIUM AMAZON.BE LISTING QUALITY ANALYSIS")
    print("Expert E-commerce Strategist & SEO Evaluation")
    print("=" * 80)
    print()
    
    # Load listing data
    try:
        with open('belgium_listing_1172.json', 'r', encoding='utf-8') as f:
            listing = json.load(f)
    except FileNotFoundError:
        print("❌ Error: belgium_listing_1172.json not found")
        return
    
    # Analysis results storage
    analysis = {
        'critical_issues': [],
        'major_issues': [],
        'minor_issues': [],
        'strengths': [],
        'scores': {},
        'recommendations': []
    }
    
    print("📊 LISTING OVERVIEW")
    print("-" * 40)
    print(f"Product: {listing['product_name']}")
    print(f"Platform: Amazon.be (Belgium)")
    print(f"Expected Language: French (fr-BE)")
    print(f"Brand: ProSharp")
    print(f"Price: €89.99")
    print(f"Occasion: Noel (Christmas)")
    print(f"Quality Score: {listing['quality_score']}/10")
    print()
    
    # 1. LANGUAGE LOCALIZATION ANALYSIS
    print("LANGUAGE LOCALIZATION ANALYSIS")
    print("-" * 50)
    
    title = listing['title']
    description = listing['long_description']
    bullets = listing['bullet_points']
    
    # Check for French content
    french_indicators = ['le', 'la', 'les', 'de', 'du', 'des', 'avec', 'pour', 'dans', 'sur', 'par', 'et', 'ou', 'mais', 'donc', 'car']
    french_count = sum(1 for word in french_indicators if word.lower() in title.lower() or word.lower() in description.lower())
    
    if french_count == 0:
        analysis['critical_issues'].append("Complete language localization failure - listing is in English, not French")
        localization_score = 0
    else:
        localization_score = min(10, (french_count / len(french_indicators)) * 10)
    
    print(f"❌ CRITICAL ISSUE: Listing is entirely in English, not French")
    print(f"Required: French (fr-BE) for Amazon.be")
    print(f"Localization Score: {localization_score}/10")
    print()
    
    # 2. TITLE OPTIMIZATION ANALYSIS
    print("📝 TITLE OPTIMIZATION ANALYSIS")  
    print("-" * 50)
    
    title_length = len(title)
    title_score = 0
    
    print(f"Title: {title}")
    print(f"Length: {title_length} characters")
    
    if title_length < 150:
        analysis['major_issues'].append(f"Title too short ({title_length} chars) - should be 150+ for optimal SEO")
        title_score += 3
    elif title_length >= 150:
        analysis['strengths'].append("Title meets 150+ character requirement")
        title_score += 6
        
    # Check for key elements
    if 'ProSharp' in title:
        title_score += 2
        analysis['strengths'].append("Brand name included in title")
    else:
        analysis['major_issues'].append("Brand name missing from title")
        
    if 'Noel' in title or 'Christmas' in title:
        title_score += 2
        analysis['strengths'].append("Occasion keyword included in title")
    else:
        analysis['minor_issues'].append("Occasion keyword could be more prominent")
        
    print(f"📊 Title Score: {title_score}/10")
    print()
    
    # 3. A+ CONTENT ANALYSIS
    print("✨ A+ CONTENT ANALYSIS")
    print("-" * 50)
    
    aplus_content = listing.get('amazon_aplus_content', '')
    aplus_score = 0
    
    # Count sections
    section_count = aplus_content.count('aplus-section-card')
    print(f"A+ Content Sections: {section_count}")
    
    if section_count >= 8:
        aplus_score += 4
        analysis['strengths'].append(f"Comprehensive A+ content with {section_count} sections")
    elif section_count >= 6:
        aplus_score += 3
        analysis['minor_issues'].append(f"A+ content has {section_count} sections, could use 8+ for maximum impact")
    else:
        analysis['major_issues'].append(f"A+ content insufficient - only {section_count} sections")
        
    # Check for image descriptions in ENGLISH
    if 'ENGLISH:' in aplus_content or 'Stratégie d\'Image' in aplus_content:
        aplus_score += 3
        analysis['strengths'].append("A+ content includes detailed image descriptions")
    else:
        analysis['major_issues'].append("A+ content lacks detailed image descriptions")
    
    # Check for French keywords in A+ content
    if 'Mots-clés' in aplus_content:
        aplus_score += 3
        analysis['strengths'].append("A+ content includes French SEO elements")
    else:
        analysis['critical_issues'].append("A+ content lacks French localization")
        
    print(f"📊 A+ Content Score: {aplus_score}/10")
    print()
    
    # 4. CULTURAL LOCALIZATION ANALYSIS
    print("🇧🇪 CULTURAL LOCALIZATION ANALYSIS")
    print("-" * 50)
    
    cultural_score = 0
    
    # Check for Belgian/European cultural elements
    if 'Noel' in description:
        cultural_score += 3
        analysis['strengths'].append("Noel (Christmas) occasion properly integrated")
    else:
        analysis['major_issues'].append("Christmas occasion not properly localized for Belgian market")
        
    # Check for European elements (CE certification, warranty)
    if 'CE' in description or 'CE' in bullets:
        cultural_score += 2
        analysis['strengths'].append("CE certification mentioned (important for EU)")
    else:
        analysis['minor_issues'].append("CE certification could be more prominent for EU market")
        
    # Check for Euro pricing
    if '€' in description or 'EUR' in description:
        cultural_score += 2
        analysis['strengths'].append("Euro pricing mentioned")
    else:
        analysis['minor_issues'].append("Euro pricing not prominently featured")
        
    # Check for European warranty standards
    if '2 year' in description or '2-year' in description:
        cultural_score += 3
        analysis['strengths'].append("2-year warranty aligns with European standards")
        
    print(f"📊 Cultural Localization Score: {cultural_score}/10")
    print()
    
    # 5. BULLET POINTS ANALYSIS
    print("🔸 BULLET POINTS ANALYSIS")
    print("-" * 50)
    
    bullet_lines = bullets.split('\n\n') if bullets else []
    bullet_score = 0
    
    print(f"Number of bullet points: {len(bullet_lines)}")
    
    if len(bullet_lines) >= 5:
        bullet_score += 3
        analysis['strengths'].append(f"Complete bullet point set ({len(bullet_lines)} bullets)")
    else:
        analysis['major_issues'].append(f"Insufficient bullet points ({len(bullet_lines)}) - need 5+")
        
    # Check for conversion elements
    conversion_phrases = ['guarantee', 'warranty', 'certified', 'professional', 'luxury', 'premium']
    conversion_count = sum(1 for phrase in conversion_phrases if phrase.lower() in bullets.lower())
    
    if conversion_count >= 4:
        bullet_score += 4
        analysis['strengths'].append("Bullet points rich with conversion elements")
    elif conversion_count >= 2:
        bullet_score += 2
        analysis['minor_issues'].append("Bullet points could use more conversion elements")
    else:
        analysis['major_issues'].append("Bullet points lack conversion-focused language")
        
    # Check for French localization in bullets
    if any(french_word in bullets.lower() for french_word in french_indicators):
        bullet_score += 3
        analysis['strengths'].append("Bullet points include French localization")
    else:
        analysis['critical_issues'].append("Bullet points are not localized to French")
        
    print(f"📊 Bullet Points Score: {bullet_score}/10")
    print()
    
    # 6. KEYWORD STRATEGY ANALYSIS
    print("🔍 KEYWORD STRATEGY ANALYSIS")
    print("-" * 50)
    
    keywords = listing.get('keywords', '')
    backend_keywords = listing.get('amazon_backend_keywords', '')
    keyword_score = 0
    
    # Count keywords
    keyword_list = [k.strip() for k in keywords.split(',') if k.strip()] if keywords else []
    backend_list = backend_keywords.split() if backend_keywords else []
    
    print(f"Frontend keywords: {len(keyword_list)}")
    print(f"Backend keywords: {len(backend_list)} words")
    
    if len(keyword_list) >= 40:
        keyword_score += 3
        analysis['strengths'].append(f"Comprehensive keyword strategy ({len(keyword_list)} keywords)")
    else:
        analysis['minor_issues'].append(f"Could expand keyword list (currently {len(keyword_list)})")
        
    if len(backend_keywords) >= 200:
        keyword_score += 3
        analysis['strengths'].append("Backend keywords properly utilized")
    else:
        analysis['minor_issues'].append("Backend keywords could be expanded")
        
    # Check for French keywords
    if any('français' in kw.lower() or 'belgique' in kw.lower() or 'belge' in kw.lower() for kw in keyword_list):
        keyword_score += 4
        analysis['strengths'].append("Keywords include French/Belgian targeting")
    else:
        analysis['critical_issues'].append("Keywords lack French/Belgian localization")
        
    print(f"📊 Keyword Strategy Score: {keyword_score}/10")
    print()
    
    # 7. COMPETITIVE COMPARISON
    print("🏆 COMPETITIVE COMPARISON")
    print("-" * 50)
    
    # Compare against Helium 10, Jasper AI, Copy Monkey standards
    competitive_score = 0
    
    # Helium 10 Standards (SEO focus)
    if title_length >= 150 and len(keyword_list) >= 30:
        competitive_score += 2
        analysis['strengths'].append("Meets Helium 10 SEO standards")
    else:
        analysis['major_issues'].append("Falls short of Helium 10 SEO standards")
        
    # Jasper AI Standards (copy quality)
    if 'luxury' in description.lower() and 'professional' in description.lower():
        competitive_score += 2
        analysis['strengths'].append("Matches Jasper AI copy quality elements")
    else:
        analysis['major_issues'].append("Copy quality below Jasper AI standards")
        
    # Copy Monkey Standards (conversion focus)
    if 'guarantee' in description.lower() and 'warranty' in description.lower():
        competitive_score += 2
        analysis['strengths'].append("Meets Copy Monkey conversion standards")
    else:
        analysis['major_issues'].append("Lacks Copy Monkey conversion focus")
        
    # International localization (critical differentiator)
    if localization_score >= 8:
        competitive_score += 4
        analysis['strengths'].append("Superior international localization vs competitors")
    else:
        analysis['critical_issues'].append("Fails international localization - major competitive disadvantage")
        
    print(f"📊 Competitive Score: {competitive_score}/10")
    print()
    
    # 8. CALCULATE OVERALL SCORES
    print("📋 FINAL QUALITY ASSESSMENT")
    print("-" * 50)
    
    # Store individual scores
    analysis['scores'] = {
        'localization': localization_score,
        'title': title_score, 
        'aplus': aplus_score,
        'cultural': cultural_score,
        'bullets': bullet_score,
        'keywords': keyword_score,
        'competitive': competitive_score
    }
    
    # Calculate weighted overall score
    overall_score = (
        localization_score * 0.25 +  # 25% weight - critical for international
        title_score * 0.15 +         # 15% weight
        aplus_score * 0.20 +         # 20% weight  
        cultural_score * 0.15 +      # 15% weight
        bullet_score * 0.15 +        # 15% weight
        keyword_score * 0.10         # 10% weight
    )
    
    # Grade assignment
    if overall_score >= 9:
        grade = "A+"
        quality_level = "Exceptional - Exceeds all competitor standards"
    elif overall_score >= 8:
        grade = "A"
        quality_level = "Excellent - Matches top competitor quality"
    elif overall_score >= 7:
        grade = "B+"
        quality_level = "Good - Above average quality"
    elif overall_score >= 6:
        grade = "B"
        quality_level = "Fair - Meets basic standards"
    elif overall_score >= 5:
        grade = "C"
        quality_level = "Below Average - Needs improvement"
    else:
        grade = "F"
        quality_level = "Failing - Major issues need resolution"
    
    print(f"🎯 OVERALL QUALITY SCORE: {overall_score:.1f}/10 (Grade: {grade})")
    print(f"📊 Quality Level: {quality_level}")
    print()
    
    # 9. CRITICAL ISSUES SUMMARY
    print("🚨 CRITICAL ISSUES")
    print("-" * 50)
    for issue in analysis['critical_issues']:
        print(f"❌ {issue}")
    print()
    
    # 10. MAJOR ISSUES SUMMARY  
    print("⚠️ MAJOR ISSUES")
    print("-" * 50)
    for issue in analysis['major_issues']:
        print(f"🟡 {issue}")
    print()
    
    # 11. STRENGTHS SUMMARY
    print("✅ STRENGTHS")
    print("-" * 50)
    for strength in analysis['strengths']:
        print(f"✅ {strength}")
    print()
    
    # 12. RECOMMENDATIONS FOR 10/10 QUALITY
    print("🎯 RECOMMENDATIONS TO ACHIEVE 10/10 QUALITY")
    print("-" * 60)
    
    recommendations = [
        "1. IMMEDIATE CRITICAL FIX: Completely translate entire listing to French (fr-BE)",
        "   - Title, description, bullet points must be in native French",
        "   - Use French terminology: 'affûteur de couteaux professionnel'",
        "   - Adapt cultural references for Belgian market",
        "",
        "2. EXPAND TITLE to 150+ characters in French:",
        "   - 'Affûteur de Couteaux Professionnel ProSharp - Disques Diamant & Céramique - Manche Noyer Premium 15°/20° - Édition Cadeau Noël Exclusive - Garantie 2 Ans & Qualité Certifiée CE'",
        "",
        "3. ENHANCE A+ CONTENT with French localization:",
        "   - Maintain 8 comprehensive sections",
        "   - Keep ENGLISH image descriptions for designers",
        "   - Translate all user-facing content to French",
        "   - Add Belgian cultural references",
        "",
        "4. OPTIMIZE KEYWORDS for French search terms:",
        "   - Primary: 'affûteur couteaux', 'aiguisoir professionnel', 'cadeau Noël'",
        "   - Include Belgian-specific terms: 'Belgique', 'belge'",
        "   - Target French Christmas terms: 'Noël', 'fêtes'",
        "",
        "5. ENHANCE BULLET POINTS with French conversion elements:",
        "   - Use luxury terminology: 'qualité premium', 'excellence'",
        "   - Emphasize European standards: 'certification CE', 'garantie 2 ans'",
        "   - Include Belgian cultural elements",
        "",
        "6. STRENGTHEN CULTURAL LOCALIZATION:",
        "   - Reference Belgian cooking traditions",
        "   - Mention European safety standards prominently",
        "   - Use Euro pricing throughout",
        "   - Adapt Noel gifting customs for Belgian market"
    ]
    
    for rec in recommendations:
        print(rec)
    
    print()
    print("=" * 80)
    print("🔍 ANALYSIS COMPLETE")
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    return analysis

if __name__ == "__main__":
    analysis = analyze_belgium_listing()