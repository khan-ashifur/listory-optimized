"""
Advanced Brand Tone Optimizer - Ensures 10/10 Quality Differentiation
Each brand tone gets completely different vocabulary, style, and approach
"""

import random

class BrandToneOptimizer:
    """Handles brand tone-specific optimizations for perfect differentiation"""
    
    def __init__(self):
        self.tone_configurations = {
            "professional": {
                "title_starters": [
                    "Professional-Grade",
                    "Industry-Leading", 
                    "Expert-Approved",
                    "Certified Professional",
                    "Pro-Level",
                    "Advanced Professional"
                ],
                "power_words": [
                    "professional", "proven", "reliable", "expert", "advanced", 
                    "precision", "certified", "industry-standard", "dependable",
                    "engineered", "tested", "validated", "optimized", "calibrated"
                ],
                "bullet_labels": [
                    "PROFESSIONAL PERFORMANCE:",
                    "EXPERT ENGINEERING:",
                    "PROVEN RELIABILITY:",
                    "INDUSTRY STANDARD:",
                    "PRECISION BUILT:",
                    "CERTIFIED QUALITY:",
                    "ADVANCED DESIGN:",
                    "TESTED DURABILITY:"
                ],
                "bullet_labels_de": [
                    "PROFESSIONELLE LEISTUNG:",
                    "EXPERTEN-KONSTRUKTION:",
                    "BEWÄHRTE ZUVERLÄSSIGKEIT:",
                    "INDUSTRIE-STANDARD:",
                    "PRÄZISIONS-FERTIGUNG:",
                    "ZERTIFIZIERTE QUALITÄT:",
                    "FORTSCHRITTLICHES DESIGN:",
                    "GETESTETE LANGLEBIGKEIT:"
                ],
                "description_hooks": [
                    "As professionals in this industry know,",
                    "Expert analysis reveals",
                    "Professional testing confirms", 
                    "Industry standards require",
                    "Technical specifications prove"
                ],
                "avoid_words": ["revolutionary", "game-changing", "cutting-edge", "breakthrough"],
                "tone_enforcement": "MANDATORY: Use at least 3 professional/expert terms in title and 5+ across bullets"
            },
            
            "casual": {
                "title_starters": [
                    "Super Easy",
                    "Just Perfect",
                    "Love This",
                    "Simply Great",
                    "Really Good",
                    "So Simple"
                ],
                "power_words": [
                    "easy", "simple", "love", "great", "perfect", "awesome",
                    "friendly", "comfortable", "convenient", "effortless",
                    "straightforward", "user-friendly", "hassle-free", "smooth", "relaxed"
                ],
                "bullet_labels": [
                    "SUPER EASY TO USE:",
                    "YOU'LL LOVE THIS:",
                    "JUST PERFECT FOR:",
                    "SO SIMPLE:",
                    "REALLY CONVENIENT:",
                    "MAKES LIFE EASIER:",
                    "TOTALLY STRESS-FREE:",
                    "JUST WORKS GREAT:"
                ],
                "bullet_labels_de": [
                    "SUPER EINFACH ZU BEDIENEN:",
                    "DAS WERDEN SIE LIEBEN:",
                    "EINFACH PERFEKT FÜR:",
                    "SO EINFACH:",
                    "WIRKLICH PRAKTISCH:",
                    "MACHT DAS LEBEN LEICHTER:",
                    "VÖLLIG STRESSFREI:",
                    "FUNKTIONIERT EINFACH SUPER:"
                ],
                "description_hooks": [
                    "You know what's great about this?",
                    "Here's what makes this so easy:",
                    "Love how simple this is:",
                    "This just makes sense:",
                    "Perfect for when you want"
                ],
                "avoid_words": ["complex", "sophisticated", "technical", "advanced"],
                "tone_enforcement": "MANDATORY: Use conversational, friendly language throughout. Sound like talking to a friend."
            },
            
            "luxury": {
                "title_starters": [
                    "Premium",
                    "Luxury",
                    "Elegant",
                    "Sophisticated", 
                    "Exclusive",
                    "Refined"
                ],
                "power_words": [
                    "premium", "luxury", "elegant", "sophisticated", "exclusive",
                    "refined", "exquisite", "superior", "exceptional", "prestigious",
                    "crafted", "curated", "elevated", "distinguished", "opulent"
                ],
                "bullet_labels": [
                    "PREMIUM CRAFTSMANSHIP:",
                    "LUXURY EXPERIENCE:",
                    "ELEGANT DESIGN:",
                    "SOPHISTICATED PERFORMANCE:",
                    "EXCLUSIVE FEATURES:",
                    "REFINED QUALITY:",
                    "EXCEPTIONAL VALUE:",
                    "DISTINGUISHED STYLE:"
                ],
                "bullet_labels_de": [
                    "PREMIUM HANDWERKSKUNST:",
                    "LUXURIÖSES ERLEBNIS:",
                    "ELEGANTES DESIGN:",
                    "HOCHWERTIGE LEISTUNG:",
                    "EXKLUSIVE FUNKTIONEN:",
                    "RAFFINIERTE QUALITÄT:",
                    "AUSSERGEWÖHNLICHER WERT:",
                    "DISTINGUIERTER STIL:"
                ],
                "description_hooks": [
                    "True luxury lies in the details.",
                    "Sophisticated design meets exceptional performance.",
                    "Experience the difference premium quality makes.",
                    "Elevate your expectations with",
                    "Discover what sophisticated engineering creates."
                ],
                "avoid_words": ["cheap", "basic", "simple", "ordinary"],
                "tone_enforcement": "MANDATORY: Use elegant, sophisticated vocabulary. Focus on quality and craftsmanship."
            },
            
            "playful": {
                "title_starters": [
                    "Super Cool",
                    "Amazing",
                    "Fun & Smart",
                    "Cleverly Designed",
                    "Surprisingly Good",
                    "Pretty Awesome"
                ],
                "power_words": [
                    "fun", "cool", "smart", "clever", "amazing", "awesome",
                    "innovative", "creative", "surprising", "delightful", "brilliant",
                    "ingenious", "witty", "charming", "engaging", "dynamic"
                ],
                "bullet_labels": [
                    "PRETTY AMAZING:",
                    "CLEVERLY DESIGNED:",
                    "SURPRISINGLY GOOD:",
                    "SUPER SMART:",
                    "REALLY COOL FEATURE:",
                    "BRILLIANTLY SIMPLE:",
                    "TOTALLY INGENIOUS:",
                    "UNEXPECTEDLY GREAT:"
                ],
                "description_hooks": [
                    "Here's something cool -",
                    "Pretty amazing how",
                    "You'll be surprised by",
                    "Clever engineering makes",
                    "Fun fact about this product:"
                ],
                "avoid_words": ["boring", "serious", "corporate", "stuffy"],
                "tone_enforcement": "MANDATORY: Use creative, energetic language that feels genuinely fun, not forced."
            },
            
            "minimal": {
                "title_starters": [
                    "Simply",
                    "Clean",
                    "Pure",
                    "Essential",
                    "Focused",
                    "Streamlined"
                ],
                "power_words": [
                    "simple", "clean", "pure", "essential", "clear", "focused",
                    "streamlined", "minimal", "purposeful", "efficient", "precise",
                    "direct", "uncluttered", "refined", "conscious"
                ],
                "bullet_labels": [
                    "SIMPLY WORKS:",
                    "CLEAN DESIGN:",
                    "PURE PERFORMANCE:",
                    "ESSENTIAL FUNCTION:",
                    "FOCUSED QUALITY:",
                    "STREAMLINED USE:",
                    "MINIMAL FUSS:",
                    "PURPOSEFUL BUILD:"
                ],
                "description_hooks": [
                    "Sometimes less really is more.",
                    "Clean design meets pure function.",
                    "Stripped of everything unnecessary.",
                    "Focus on what actually matters.",
                    "Essential quality, nothing extra."
                ],
                "avoid_words": ["complicated", "excessive", "flashy", "ornate"],
                "tone_enforcement": "MANDATORY: Keep language clean, clear, and purposeful. Less is more approach."
            },
            
            "bold": {
                "title_starters": [
                    "Powerful",
                    "Dominate",
                    "Unleash",
                    "Maximum",
                    "Ultimate",
                    "Intense"
                ],
                "power_words": [
                    "power", "dominate", "unleash", "maximum", "ultimate", "intense",
                    "strong", "bold", "aggressive", "commanding", "forceful",
                    "dynamic", "robust", "vigorous", "potent", "mighty"
                ],
                "bullet_labels": [
                    "MAXIMUM POWER:",
                    "UNLEASH PERFORMANCE:",
                    "DOMINATE WITH:",
                    "ULTIMATE STRENGTH:",
                    "INTENSE RESULTS:",
                    "POWERFUL DESIGN:",
                    "BOLD PERFORMANCE:",
                    "COMMANDING PRESENCE:"
                ],
                "description_hooks": [
                    "Power through any challenge with",
                    "Dominate your field using",
                    "Unleash the full potential of",
                    "Maximum performance demands",
                    "Bold engineering delivers"
                ],
                "avoid_words": ["weak", "gentle", "subtle", "soft"],
                "tone_enforcement": "MANDATORY: Use strong, commanding language that conveys power and confidence."
            }
        }
    
    def get_brand_tone_enhancement(self, brand_tone, marketplace='us'):
        """Get comprehensive brand tone enhancement prompt"""
        
        if brand_tone not in self.tone_configurations:
            brand_tone = "professional"  # Default fallback
            
        config = self.tone_configurations[brand_tone]
        
        # Randomly select elements for variety
        title_starter = random.choice(config["title_starters"])
        power_words = random.sample(config["power_words"], min(5, len(config["power_words"])))
        
        # Use German labels for German marketplace
        if marketplace == 'de' and "bullet_labels_de" in config:
            bullet_labels = random.sample(config["bullet_labels_de"], min(4, len(config["bullet_labels_de"])))
        else:
            bullet_labels = random.sample(config["bullet_labels"], min(4, len(config["bullet_labels"])))
            
        description_hook = random.choice(config["description_hooks"])
        
        enhancement = f"""
🎨 CRITICAL BRAND TONE OPTIMIZATION FOR {brand_tone.upper()} 🎨

This listing MUST sound completely different from other brand tones.
Generic content will be rejected. Each element must reflect {brand_tone} personality.

MANDATORY TITLE REQUIREMENTS:
- Start with or include: "{title_starter}" or similar {brand_tone} language
- MUST use 2+ of these power words: {', '.join(power_words[:3])}
- Avoid these words completely: {', '.join(config['avoid_words'])}
- Sound distinctly {brand_tone}, not generic

MANDATORY BULLET POINT REQUIREMENTS:
- Use these label styles: {', '.join(bullet_labels[:2])}
- Each bullet MUST sound {brand_tone} in personality
- Include these power words throughout: {', '.join(power_words)}
- Vary bullet structure but maintain {brand_tone} voice

MANDATORY DESCRIPTION REQUIREMENTS:
- Start with: "{description_hook}" or similar {brand_tone} opening
- Use {brand_tone} vocabulary throughout: {', '.join(power_words[:4])}
- Maintain {brand_tone} personality consistently
- Avoid generic marketing speak

MANDATORY A+ CONTENT REQUIREMENTS:
- Hero title must sound {brand_tone}: include power words
- All sections must maintain {brand_tone} voice consistently  
- Use {brand_tone}-appropriate language in every element

{config['tone_enforcement']}

TONE VALIDATION CHECKLIST:
□ Title includes {brand_tone} starter words or power words
□ Bullets use {brand_tone}-specific labels and vocabulary
□ Description opens with {brand_tone} hook and maintains voice
□ A+ content reflects {brand_tone} personality throughout
□ All avoided words are completely absent
□ Content sounds distinctly {brand_tone}, not generic

CRITICAL SUCCESS FACTOR:
A person reading this listing should immediately recognize it as {brand_tone} 
brand tone without being told. The vocabulary, style, and approach must be 
unmistakably {brand_tone} throughout every element.
"""
        
        return enhancement
    
    def get_tone_specific_json_structure(self, brand_tone):
        """Get tone-specific JSON structure modifications"""
        
        config = self.tone_configurations.get(brand_tone, self.tone_configurations["professional"])
        
        structure_mods = {
            "title_instruction": f"Write {brand_tone} title using power words: {', '.join(config['power_words'][:3])}",
            "bullet_instruction": f"Use {brand_tone} bullet labels like: {', '.join(config['bullet_labels'][:2])}",
            "description_instruction": f"Start with {brand_tone} hook and maintain {brand_tone} voice throughout"
        }
        
        return structure_mods