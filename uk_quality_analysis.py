#!/usr/bin/env python3
"""
UK Market Quality Analysis Tool
Analyzes UK listing implementation against Mexico's proven 10/10 structure
"""

def analyze_uk_quality(title, bullets, description):
    """Analyze UK listing quality against competitor standards"""
    
    # Critical UK formality phrases that MUST be present
    uk_formality_phrases = [
        "we're delighted to offer",
        "rest assured", 
        "you'll find",
        "we're confident",
        "proudly british",
        "british standards",
        "uk warranty",
        "ce marked"
    ]
    
    # Mexico's proven ★ bullet pattern structure
    mexico_bullet_patterns = [
        "★ PREMIUM",
        "★ SUPERIOR", 
        "★ EXCEPTIONAL",
        "★ GUARANTEED",
        "★ TRUSTED"
    ]
    
    # Emotional intensity words from Mexico's success
    emotional_words = [
        "incredible", "amazing", "exceptional", "outstanding",
        "brilliant", "superb", "magnificent", "extraordinary"
    ]
    
    # Initialize scores
    scores = {
        'british_formality': 0,
        'mexico_bullets': 0,
        'emotion_score': 0,
        'description_quality': 0,
        'overall': 0
    }
    
    # 1. Check British formality phrases
    formality_count = 0
    content_to_check = f"{title} {' '.join(bullets)} {description}".lower()
    
    for phrase in uk_formality_phrases:
        if phrase.lower() in content_to_check:
            formality_count += 1
    
    scores['british_formality'] = min(10, formality_count * 2)
    
    # 2. Check Mexico bullet pattern structure
    bullet_pattern_count = 0
    for bullet in bullets:
        if bullet.strip().startswith('★'):
            bullet_pattern_count += 1
    
    scores['mexico_bullets'] = min(10, bullet_pattern_count * 2)
    
    # 3. Check emotional intensity
    emotion_count = 0
    for word in emotional_words:
        if word.lower() in content_to_check:
            emotion_count += 1
    
    scores['emotion_score'] = min(10, emotion_count * 1.5)
    
    # 4. Description quality (length, structure, CTAs)
    desc_score = 0
    if len(description) > 800:  # Good length
        desc_score += 3
    if "buy now" in description.lower() or "order today" in description.lower():
        desc_score += 2
    if "guarantee" in description.lower():
        desc_score += 2
    if "british" in description.lower():
        desc_score += 3
    
    scores['description_quality'] = min(10, desc_score)
    
    # Calculate overall score
    scores['overall'] = (scores['british_formality'] + scores['mexico_bullets'] + 
                        scores['emotion_score'] + scores['description_quality']) / 4
    
    return scores

def generate_uk_recommendations():
    """Generate specific recommendations to achieve 10/10 quality"""
    
    recommendations = {
        'critical_fixes': [
            "ENFORCE star bullet pattern in ALL 5 bullets (copy Mexico exactly)",
            "MANDATE British formality phrases in every bullet",
            "Increase emotional intensity with Mexico's proven words",
            "Strengthen UK prompt to override generic AI patterns"
        ],
        
        'bullet_enhancement': [
            "Pattern 1: STAR PREMIUM BRITISH EXCELLENCE: [Feature] engineered to British standards for [superior result]. We're confident you'll appreciate [refined benefit].",
            "Pattern 2: STAR HERITAGE QUALITY ASSURED: [Traditional aspect] combining British craftsmanship with [modern innovation]. Rest assured, [quality guarantee].",
            "Pattern 3: STAR PERFECT FOR BRITISH LIFESTYLE: [Feature] ideal for British homes and [lifestyle scenario]. You'll find it exceptional for [specific UK use].",
            "Pattern 4: STAR TRUSTED BY UK FAMILIES: [Social proof] thousands of British customers who value [quality aspect]. We're delighted to offer [exclusive benefit].",
            "Pattern 5: STAR BRILLIANT GIFT CHOICE: [Gift aspect] for [UK occasion/person]. Proudly presented with [British service/packaging]."
        ],
        
        'prompt_strengthening': [
            "Add MANDATORY requirements section at top of UK prompt",
            "Use triple emphasis for critical requirements",
            "Include specific bullet templates with [variables] to fill",
            "Add penalty warnings for non-compliance",
            "Include competitor comparison standards"
        ],
        
        'emotional_enhancement': [
            "Replace 'good' with 'brilliant', 'excellent' with 'exceptional'",
            "Use British superlatives: 'absolutely brilliant', 'truly outstanding'",
            "Add excitement: 'you'll be delighted', 'prepare to be amazed'",
            "Include urgency: 'limited time', 'while stocks last'"
        ],
        
        'cultural_integration': [
            "Reference Boxing Day, Sunday roast, afternoon tea",
            "Include weather references: 'British climate tested'",
            "Mention British innovations and heritage",
            "Use location pride: 'from London to Edinburgh'",
            "Include social aspects: 'perfect for pub nights'"
        ]
    }
    
    return recommendations

def compare_to_competitors():
    """Compare against Helium 10, Jasper AI, and CopyMonkey"""
    
    competitor_analysis = {
        'helium_10': {
            'strengths': ['Keyword optimization', 'Data-driven approach'],
            'weaknesses': ['Generic copy', 'Low emotional engagement', 'No cultural adaptation'],
            'our_advantage': 'Superior cultural localization + emotional engagement'
        },
        
        'jasper_ai': {
            'strengths': ['Good copywriting', 'Decent structure'],
            'weaknesses': ['Generic templates', 'No market-specific adaptation', 'Lacks British formality'],
            'our_advantage': 'Market-specific formality phrases + proven Mexico structure'
        },
        
        'copymonkey': {
            'strengths': ['Technical optimization', 'SEO focus'],
            'weaknesses': ['Boring copy', 'No emotional appeal', 'Template-based'],
            'our_advantage': 'Emotional conversion power + cultural authenticity'
        }
    }
    
    return competitor_analysis

if __name__ == "__main__":
    # Example UK listing analysis
    sample_title = "Premium Gaming Headset - Professional Audio Quality - UK Warranty"
    
    sample_bullets = [
        "High-quality audio with noise cancellation technology",
        "Comfortable design for extended gaming sessions", 
        "Long battery life up to 30 hours of use",
        "Wireless Bluetooth connectivity with all devices",
        "Includes UK warranty and customer support"
    ]
    
    sample_description = "This gaming headset offers great sound quality and comfort for gamers. Features include noise cancellation and long battery life."
    
    # Analyze quality
    scores = analyze_uk_quality(sample_title, sample_bullets, sample_description)
    
    print("UK MARKET QUALITY ANALYSIS")
    print("=" * 50)
    print(f"British Formality Score: {scores['british_formality']}/10")
    print(f"Mexico Bullet Pattern Score: {scores['mexico_bullets']}/10")
    print(f"Emotion Score: {scores['emotion_score']}/10")
    print(f"Description Quality Score: {scores['description_quality']}/10")
    print(f"OVERALL SCORE: {scores['overall']:.1f}/10")
    
    if scores['overall'] < 7:
        print("\nCRITICAL QUALITY ISSUES DETECTED")
        
    # Generate recommendations
    recommendations = generate_uk_recommendations()
    
    print("\nRECOMMENDATIONS FOR 10/10 QUALITY:")
    print("\nCRITICAL FIXES:")
    for fix in recommendations['critical_fixes']:
        print(f"  {fix}")
        
    print("\nENHANCED BULLET PATTERNS:")
    for i, pattern in enumerate(recommendations['bullet_enhancement'], 1):
        print(f"  {i}. {pattern}")
    
    # Competitor comparison
    competitors = compare_to_competitors()
    
    print("\nCOMPETITIVE ADVANTAGE ANALYSIS:")
    for competitor, analysis in competitors.items():
        print(f"\n{competitor.upper()}:")
        print(f"  Our Advantage: {analysis['our_advantage']}")
        print(f"  Their Weakness: {', '.join(analysis['weaknesses'])}")