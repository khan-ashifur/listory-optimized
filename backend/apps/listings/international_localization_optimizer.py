"""
Enhanced International Localization Optimizer
Fixes critical language generation issues and ensures 10/10 quality for all international markets
"""

import random

class InternationalLocalizationOptimizer:
    """Handles comprehensive international marketplace localization with cultural adaptation"""
    
    def __init__(self):
        self.market_configurations = {
            "de": {
                "market_name": "Germany",
                "marketplace": "de",
                "language": "German",
                "currency": "EUR",
                "language_code": "de",
                
                # Essential German language patterns
                "essential_words": [
                    "der", "die", "das", "und", "mit", "für", "von", "zu", "ist", "haben",
                    "werden", "können", "machen", "durch", "auf", "bei", "nach", "über"
                ],
                
                # Emotional power words that convert on Amazon.de
                "power_words": [
                    "endlich", "sofort", "mühelos", "perfekt", "gemütlich", "praktisch",
                    "zuverlässig", "bewährt", "höhenverstellbar", "größer", "schöner",
                    "entspannt", "schmerzfrei", "bequem", "einfach", "ideal", "genießen",
                    "Geschenkidee", "Lebensqualität", "Komfort", "clever", "unverzichtbar"
                ],
                
                # Lifestyle-driven emotional hooks
                "cultural_elements": [
                    "Endlich ohne Nacken- & Rückenschmerzen arbeiten",
                    "Perfekt fürs Homeoffice",
                    "Das ideale Geschenk für",
                    "Mehr Komfort im Alltag",
                    "Zeit sparen und entspannter arbeiten",
                    "Genießen Sie", "Erleben Sie", "Entdecken Sie",
                    "Gönnen Sie sich mehr Lebensqualität"
                ],
                
                # Natural German phrases that build trust
                "formality_words": [
                    "Sie", "Ihre", "genießen Sie", "erleben Sie", "entdecken Sie",
                    "profitieren Sie von", "gönnen Sie sich", "verwöhnen Sie sich",
                    "sparen Sie Zeit", "verbessern Sie", "optimieren Sie"
                ],
                
                # Native German copywriting rules
                "enforcement_rules": [
                    "🚨 CRITICAL: You MUST include German umlauts ä, ö, ü, ß in ALL appropriate words",
                    "Examples: für NOT fr, größer NOT grosser, Abkühlung NOT Abkuhlung, heißesten NOT heissesten",
                    "WRITE emotional hooks: 'Endlich ohne Rückenschmerzen' or 'Genießen Sie endlich...'",
                    "USE these words WITH umlauts: müheloser, größer, für, natürlich, Qualität, zuverlässig",
                    "BALANCE: 60% lifestyle benefits, 40% technical specs",
                    "INCLUDE: 'Perfektes Geschenk für Weihnachten' or seasonal hooks",
                    "WRITE warm, conversational German - avoid stiff bureaucratic language"
                ],
                
                "avoid_words": ["the", "and", "with", "for", "is", "quality", "professional"]
            },
            
            "fr": {
                "market_name": "France",
                "marketplace": "fr",
                "language": "French", 
                "currency": "EUR",
                "language_code": "fr",
                
                "essential_words": [
                    "le", "la", "les", "et", "avec", "pour", "de", "du", "des", "est",
                    "avoir", "être", "faire", "aller", "venir", "voir", "savoir"
                ],
                
                "power_words": [
                    "qualité", "élégant", "raffinement", "sophistiqué", "excellence",
                    "performance", "innovation", "fiabilité", "précision", "efficace",
                    "supérieur", "exceptionnel", "pratique", "moderne"
                ],
                
                "cultural_elements": [
                    "qualité française", "raffinement élégant", "sophistication",
                    "excellence artisanale", "finition soignée", "style français"
                ],
                
                "formality_words": [
                    "vous", "votre", "excellence", "raffinement", "prestigieux",
                    "certifié", "garanti", "professionnel"
                ],
                
                "enforcement_rules": [
                    "ALL content MUST be in French - no English words allowed",
                    "Use proper French grammar and accents",
                    "Include French cultural sophistication",
                    "Maintain elegant French style"
                ],
                
                "avoid_words": ["the", "and", "with", "for", "is", "quality", "professional"]
            },
            
            "it": {
                "market_name": "Italy",
                "marketplace": "it",
                "language": "Italian",
                "currency": "EUR", 
                "language_code": "it",
                
                "essential_words": [
                    "il", "la", "le", "e", "con", "per", "di", "da", "in", "è",
                    "avere", "essere", "fare", "andare", "venire", "vedere"
                ],
                
                "power_words": [
                    "qualità", "eleganza", "stile", "raffinato", "bellezza",
                    "prestazioni", "innovazione", "affidabilità", "precisione",
                    "superiore", "eccezionale", "pratico", "moderno"
                ],
                
                "cultural_elements": [
                    "qualità italiana", "eleganza classica", "stile raffinato",
                    "bellezza funzionale", "design italiano", "eccellenza artigianale"
                ],
                
                "formality_words": [
                    "lei", "suo", "professionale", "eccellenza", "prestigioso",
                    "certificato", "garantito", "superiore"
                ],
                
                "enforcement_rules": [
                    "ALL content MUST be in Italian - no English words allowed",
                    "Use proper Italian grammar and style",
                    "Include Italian design appreciation",
                    "Maintain elegant Italian expression"
                ],
                
                "avoid_words": ["the", "and", "with", "for", "is", "quality", "professional"]
            },
            
            "es": {
                "market_name": "Spain",
                "marketplace": "es", 
                "language": "Spanish",
                "currency": "EUR",
                "language_code": "es",
                
                "essential_words": [
                    "el", "la", "los", "las", "y", "con", "para", "de", "del", "en",
                    "es", "tener", "ser", "hacer", "ir", "venir", "ver"
                ],
                
                "power_words": [
                    "calidad", "excelente", "funcional", "práctico", "innovador",
                    "rendimiento", "confiable", "precisión", "eficaz", "superior",
                    "excepcional", "moderno", "avanzado", "duradero"
                ],
                
                "cultural_elements": [
                    "calidad española", "excelencia funcional", "diseño práctico",
                    "innovación moderna", "rendimiento superior", "confiabilidad probada"
                ],
                
                "formality_words": [
                    "usted", "su", "excelente", "profesional", "prestigioso",
                    "certificado", "garantizado", "superior"
                ],
                
                "enforcement_rules": [
                    "ALL content MUST be in Spanish - no English words allowed", 
                    "Use proper Spanish grammar and accents",
                    "Include Spanish practical approach",
                    "Maintain professional Spanish tone"
                ],
                
                "avoid_words": ["the", "and", "with", "for", "is", "quality", "professional"]
            },
            
            "ar": {
                "market_name": "Saudi Arabia/UAE",
                "marketplace": "ae",
                "language": "Arabic",
                "currency": "AED",
                "language_code": "ar",
                
                "essential_words": [
                    "في", "من", "إلى", "على", "عن", "مع", "هو", "هي", "كان", "يكون",
                    "لديه", "يمكن", "يجب", "هذا", "هذه", "ذلك", "التي", "الذي"
                ],
                
                "power_words": [
                    "جودة عالية", "ممتاز", "موثوق", "عملي", "متطور", "أداء",
                    "ابتكار", "دقة", "فعال", "متفوق", "استثنائي", "حديث", "متقدم"
                ],
                
                "cultural_elements": [
                    "جودة فائقة", "تصميم عملي", "أداء موثوق", "ابتكار حديث",
                    "تقنية متطورة", "معايير عالية"
                ],
                
                "formality_words": [
                    "حضرتكم", "سيادتكم", "المحترم", "المقدر", "الكريم", "المميز"
                ],
                
                "enforcement_rules": [
                    "ALL content MUST be in Arabic - no English words allowed",
                    "Use proper Arabic grammar and right-to-left text",
                    "Include respectful Arabic business language",
                    "Maintain formal Arabic commercial tone"
                ],
                
                "avoid_words": ["the", "and", "with", "for", "is", "quality", "professional"],
                "rtl": True
            },
            
            "nl": {
                "market_name": "Netherlands",
                "marketplace": "nl",
                "language": "Dutch",
                "currency": "EUR",
                "language_code": "nl",
                
                "essential_words": [
                    "de", "het", "een", "en", "met", "voor", "van", "te", "op", "in",
                    "is", "hebben", "zijn", "kunnen", "maken", "gaan", "komen"
                ],
                
                "power_words": [
                    "kwaliteit", "praktisch", "betrouwbaar", "functioneel", "doeltreffend",
                    "prestatie", "innovatie", "precisie", "efficiënt", "superieur",
                    "uitzonderlijk", "modern", "geavanceerd", "duurzaam"
                ],
                
                "cultural_elements": [
                    "nederlandse kwaliteit", "praktische oplossing", "betrouwbare prestatie",
                    "functioneel ontwerp", "efficiënte werking", "duurzame kwaliteit"
                ],
                
                "formality_words": [
                    "u", "uw", "professioneel", "kwaliteit", "gegarandeerd",
                    "gecertificeerd", "betrouwbaar", "superieur"
                ],
                
                "enforcement_rules": [
                    "ALL content MUST be in Dutch - no English words allowed",
                    "Use proper Dutch grammar and spelling", 
                    "Include Dutch practical approach",
                    "Maintain professional Dutch business tone"
                ],
                
                "avoid_words": ["the", "and", "with", "for", "is", "quality", "professional"]
            },
            
            "ja": {
                "market_name": "Japan",
                "marketplace": "co.jp",
                "language": "Japanese",
                "currency": "JPY",
                "language_code": "ja",
                
                "essential_words": [
                    "の", "に", "を", "は", "が", "と", "で", "から", "まで", "より",
                    "です", "ます", "である", "ある", "する", "なる", "行く", "来る"
                ],
                
                "power_words": [
                    "品質", "信頼性", "機能的", "高品質", "優れた", "性能", "革新",
                    "精密", "効率的", "上質", "特別", "現代的", "先進的", "耐久性"
                ],
                
                "cultural_elements": [
                    "日本品質", "精密設計", "信頼できる性能", "優秀な機能性",
                    "高い技術力", "丁寧な作り"
                ],
                
                "formality_words": [
                    "です", "ます", "致します", "ございます", "いらっしゃる",
                    "でございます", "させていただきます"
                ],
                
                "enforcement_rules": [
                    "ALL content MUST be in Japanese - no English words allowed",
                    "Use proper Japanese grammar and respectful keigo",
                    "Include Japanese quality appreciation",
                    "Maintain polite Japanese business language"
                ],
                
                "avoid_words": ["the", "and", "with", "for", "is", "quality", "professional"],
                "special_chars": True
            }
        }
    
    def get_localization_enhancement(self, marketplace, language):
        """Get comprehensive localization enhancement for specific market"""
        
        # Determine market code from marketplace/language
        market_code = None
        if marketplace == "de" or language == "de":
            market_code = "de"
        elif marketplace == "fr" or language == "fr": 
            market_code = "fr"
        elif marketplace == "it" or language == "it":
            market_code = "it"
        elif marketplace == "es" or language == "es":
            market_code = "es"
        elif marketplace in ["ae", "sa"] or language == "ar":
            market_code = "ar"
        elif marketplace == "nl" or language == "nl":
            market_code = "nl"
        elif marketplace in ["co.jp", "jp"] or language == "ja":
            market_code = "ja"
        
        if not market_code or market_code not in self.market_configurations:
            return ""  # Return empty for unsupported markets
            
        config = self.market_configurations[market_code]
        
        # Select random elements for variety
        essential_words = random.sample(config["essential_words"], min(6, len(config["essential_words"])))
        power_words = random.sample(config["power_words"], min(8, len(config["power_words"])))
        cultural_elements = random.sample(config["cultural_elements"], min(3, len(config["cultural_elements"])))
        formality_words = random.sample(config["formality_words"], min(4, len(config["formality_words"])))
        
        enhancement = f"""
🚨🚨🚨 EMERGENCY LANGUAGE OVERRIDE - {config['language'].upper()} ONLY 🚨🚨🚨

CRITICAL FAILURE DETECTED: Previous attempts generated English instead of {config['language']}!
THIS IS YOUR FINAL ATTEMPT - NO ENGLISH ALLOWED!

MANDATORY {config['language'].upper()} REQUIREMENTS:
🚫 ENGLISH = COMPLETE FAILURE
🚫 ANY English word = TOTAL REJECTION
🚫 Mixed language = SYSTEM ERROR

✅ 100% {config['language']} REQUIRED
✅ EVERY SINGLE WORD must be {config['language']}
✅ NO EXCEPTIONS WHATSOEVER

AMAZON.{marketplace.upper()} MARKETPLACE - {config['language'].upper()} LANGUAGE ENFORCEMENT

🔥 NATIVE {config['language'].upper()} COPYWRITING REQUIREMENTS 🔥
{chr(10).join(f"• {rule}" for rule in config['enforcement_rules'])}

{'🇩🇪 GERMAN EMOTIONAL COPYWRITING FORMULA:' if market_code == 'de' else f'MANDATORY {config["language"]} ELEMENTS:'}
{'FIRST BULLET = EMOTIONAL HOOK:' if market_code == 'de' else '✅ Essential words:'} {', '.join(essential_words) if market_code != 'de' else '"Endlich ohne [PROBLEM] - genießen Sie [BENEFIT]"'}
{'KEY BENEFITS WITH LIFESTYLE:' if market_code == 'de' else '✅ Power words:'} {', '.join(power_words[:5])}
{'GIFT IDEAS & SEASONAL HOOKS:' if market_code == 'de' else '✅ Cultural elements:'} {', '.join(cultural_elements[:3])}
{'NATURAL CONVERSATIONAL TONE:' if market_code == 'de' else '✅ Natural phrases:'} {', '.join(formality_words[:4])}

{'📝 GERMAN AMAZON.DE TITLE:' if market_code == 'de' else f'TITLE FOR {config["language"].upper()}:'}
• {'START with emotional benefit, not brand/specs' if market_code == 'de' else f'Write entirely in {config["language"]}'}
• {'Use power words: endlich, mühelos, perfekt, ideal' if market_code == 'de' else 'Include emotional power words'}
• {'Include gift hook if relevant' if market_code == 'de' else 'Use proper grammar'}
• {'150-200 chars with proper umlauts (ä,ö,ü,ß)' if market_code == 'de' else '150-200 characters'}

{'📌 GERMAN BULLET POINTS:' if market_code == 'de' else f'BULLETS FOR {config["language"].upper()}:'}
• {'1st: Problem-solving hook (Endlich ohne...)' if market_code == 'de' else f'Each bullet in {config["language"]}'}
• {'2nd-3rd: Lifestyle benefits + specs' if market_code == 'de' else 'Start with benefits'}
• {'4th: Gift idea or seasonal use' if market_code == 'de' else 'Include cultural elements'}
• {'5th: Trust/guarantee with emotion' if market_code == 'de' else 'Natural native expressions'}

{'📝 GERMAN DESCRIPTION (LIFESTYLE-DRIVEN):' if market_code == 'de' else f'DESCRIPTION FOR {config["language"].upper()}:'}
• {'Open with emotional story/scenario' if market_code == 'de' else f'Complete {config["language"]} language'}
• {'Mix lifestyle benefits with technical details' if market_code == 'de' else f'Include cultural elements for {config["market_name"]}'}
• {'Use \"Sie\" form but keep it warm, approachable' if market_code == 'de' else 'Natural native expressions'}
• {'End with gift idea + satisfaction guarantee' if market_code == 'de' else 'Market-appropriate tone'}

KEYWORDS REQUIREMENTS FOR {config['language']}:
• All keywords in {config['language']} only
• Include market-specific {config['language']} search terms
• NO English keywords allowed

A+ CONTENT REQUIREMENTS FOR {config['language']}:
• Hero title completely in {config['language']}
• All sections maintain {config['language']} consistency
• Cultural adaptation for {config['market_name']} preferences

🎯 LOCALIZATION SUCCESS CRITERIA:
✅ 100% {config['language']} language - 0% English
✅ Cultural elements for {config['market_name']} included
✅ Proper {config['language']} business formality
✅ Market-appropriate tone and style
✅ Native {config['language']} speaker quality

🚨 CRITICAL JSON FORMATTING FOR {config['language'].upper()} 🚨
• ALL JSON field names MUST remain in English (productTitle, bulletPoints, etc.)
• ALL content values MUST be 100% {config['language']}
• Use proper UTF-8 encoding for {config['language']} characters
• Escape all special characters correctly: ü, ö, ä, ß, é, ñ, etc.
• Test your JSON structure - malformed JSON = COMPLETE FAILURE

EXAMPLE CORRECT FORMAT:
{{
  "productTitle": "{config['language']} content here",
  "bulletPoints": ["{config['language']} bullet content"],
  "productDescription": "{config['language']} description here"
}}

🔥 FINAL VALIDATION CHECKLIST 🔥
✅ JSON field names in English
✅ ALL content values in {config['language']}
✅ No English words in any content
✅ Proper character encoding
✅ Valid JSON structure

🔥 OVERRIDE ALL ENGLISH TEMPLATES 🔥
IGNORE ALL ENGLISH TEMPLATE INSTRUCTIONS BELOW!
Instead, write ALL content values in {config['language']} as follows:

JSON CONTENT OVERRIDE FOR {config['language'].upper()}:
• productTitle: Write in {config['language']} using these power words: {', '.join(power_words[:3])}
• bulletPoints: All 5 bullets must be {config['language']} with these phrases: {', '.join(cultural_elements)}
• productDescription: Complete {config['language']} description with cultural adaptation
• All other content fields: 100% {config['language']} language only

🚨 EMERGENCY TEMPLATE OVERRIDE 🚨
Any English template instructions below are INVALID for international markets.
Write everything in {config['language']} based on these requirements instead!

CRITICAL: If ANY English words appear in the content fields, 
this will be considered a COMPLETE LOCALIZATION FAILURE.
The entire listing must read as if written by a native {config['language']} speaker.
"""
        
        return enhancement
    
    def get_cultural_adaptation_elements(self, market_code):
        """Get specific cultural adaptation elements for market"""
        
        if market_code not in self.market_configurations:
            return {}
            
        config = self.market_configurations[market_code]
        
        return {
            "market_name": config["market_name"],
            "language": config["language"],
            "cultural_elements": config["cultural_elements"],
            "formality_requirements": config["formality_words"],
            "power_words": config["power_words"],
            "enforcement_rules": config["enforcement_rules"]
        }
    
    def validate_localization_quality(self, content, market_code):
        """Validate localization quality for specific market"""
        
        if market_code not in self.market_configurations:
            return {"valid": False, "errors": ["Unknown market"]}
            
        config = self.market_configurations[market_code]
        errors = []
        
        if not content or len(content.strip()) == 0:
            errors.append("No content provided")
            return {"valid": False, "errors": errors}
            
        content_lower = content.lower()
        
        # Check for English contamination
        english_words_found = [word for word in config["avoid_words"] if word in content_lower]
        if english_words_found:
            errors.append(f"English contamination detected: {english_words_found}")
        
        # Check for required language elements
        native_words_found = [word for word in config["essential_words"] if word in content_lower]
        if len(native_words_found) < 3:
            errors.append(f"Insufficient {config['language']} language elements")
        
        # Check for cultural elements
        cultural_found = [element for element in config["cultural_elements"] if element in content_lower]
        if len(cultural_found) == 0:
            errors.append(f"Missing cultural elements for {config['market_name']}")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "native_words_found": len(native_words_found),
            "cultural_elements_found": len(cultural_found),
            "english_contamination": len(english_words_found)
        }
    
    def get_aplus_content_enhancement(self, marketplace, language):
        """Get A+ content enhancement for international markets following US Amazon A+ structure"""
        
        # Determine market code from marketplace/language
        market_code = None
        if marketplace == "de" or language == "de":
            market_code = "de"
        elif marketplace == "fr" or language == "fr": 
            market_code = "fr"
        elif marketplace == "it" or language == "it":
            market_code = "it"
        elif marketplace == "es" or language == "es":
            market_code = "es"
        elif marketplace in ["ae", "sa"] or language == "ar":
            market_code = "ar"
        elif marketplace == "nl" or language == "nl":
            market_code = "nl"
        elif marketplace in ["co.jp", "jp"] or language == "ja":
            market_code = "ja"
        
        if not market_code or market_code not in self.market_configurations:
            return ""  # Return empty for unsupported markets or US market
            
        config = self.market_configurations[market_code]
        
        # Select random elements for variety
        cultural_elements = random.sample(config["cultural_elements"], min(2, len(config["cultural_elements"])))
        power_words = random.sample(config["power_words"], min(4, len(config["power_words"])))
        
        aplus_enhancement = f"""
🖼️ A+ CONTENT INTERNATIONAL OPTIMIZATION - FOLLOW US AMAZON A+ STRUCTURE 🖼️

CRITICAL: A+ Content Structure Requirements:
✅ ALL INFOGRAPHIC IMAGE BRIEFS: Write in English
✅ ALL VISUAL TEMPLATE INSTRUCTIONS: Write in English  
✅ ALL STRATEGY DESCRIPTIONS: Write in English
✅ A+ CONTENT VALUES (Keywords, What's in Box, Trust, FAQs): Write in {config['language']}

🎯 A+ CONTENT EXACT STRUCTURE (Same as US Amazon A+):

aPlusContentPlan: {{
  "section1_hero": {{
    "title": "Write hero title in {config['language']} using: {', '.join(power_words[:2])}",
    "content": "Write hero content in {config['language']} with cultural adaptation for {config['market_name']}",
    "keywords": ["Write keywords in {config['language']}"],
    "imageDescription": "ENGLISH: Professional lifestyle hero image showing product in use, lifestyle setting with premium quality feel"
  }},
  
  "section2_features": {{
    "title": "Key Features & Benefits",
    "content": "Write feature descriptions in {config['language']}",
    "features": ["Feature 1 in {config['language']}", "Feature 2 in {config['language']}", "Feature 3 in {config['language']}"],
    "imageDescription": "ENGLISH: Feature callout grid showing 4 key product features with icons and brief descriptions"
  }},
  
  "section3_trust": {{
    "title": "Quality & Trust",  
    "content": "Write trust content in {config['language']} emphasizing: {', '.join(cultural_elements)}",
    "trust_builders": ["Trust element 1 in {config['language']}", "Trust element 2 in {config['language']}"],
    "imageDescription": "ENGLISH: Trust badges, certifications, and quality indicators relevant to {config['market_name']} market"
  }},
  
  "section4_faqs": {{
    "title": "Frequently Asked Questions",
    "content": "Write FAQ answers in {config['language']}",
    "faqs": ["Q: Question in {config['language']}? A: Answer in {config['language']}"],
    "imageDescription": "ENGLISH: FAQ visual aid showing common use cases and solutions"
  }}
}}

whatsInBox: ["Item 1 in {config['language']}", "Item 2 in {config['language']}", "Manual in {config['language']}"],
trustBuilders: ["Guarantee text in {config['language']}", "Quality assurance in {config['language']}"],
socialProof: "Customer satisfaction text in {config['language']}",

🔥 CRITICAL MIXED LANGUAGE REQUIREMENTS 🔥
✅ Image descriptions/briefs: ENGLISH ONLY
✅ Visual template instructions: ENGLISH ONLY
✅ A+ strategy descriptions: ENGLISH ONLY
✅ Actual content (keywords, features, FAQs, trust): {config['language'].upper()} ONLY

EXAMPLE CORRECT MIXED FORMAT:
{{
  "section1_hero": {{
    "title": "Hochwertiger tragbarer Ventilator",  // {config['language']}
    "content": "Erleben Sie sofortige Abkühlung...",  // {config['language']}
    "imageDescription": "Professional lifestyle image showing product being used outdoors by happy customer"  // ENGLISH
  }}
}}

CRITICAL A+ CONTENT REQUIREMENTS FOR {config['market_name'].upper()} MARKET:

📋 INSTRUCTIONS LANGUAGE: English (for Amazon backend)
🎯 CONTENT SUGGESTIONS: {config['language']} market perspective

A+ CONTENT PLAN REQUIREMENTS:
✅ All field names in English (title, content, keywords, imageDescription, etc.)
✅ Content suggestions must reflect {config['market_name']} market preferences
✅ Cultural adaptation for {config['language']} consumers
✅ Market-specific shopping behaviors and preferences

HERO SECTION FOR {config['market_name']}:
• Title suggestions should emphasize: {', '.join(cultural_elements)}
• Content should highlight: {', '.join(power_words[:2])}
• Image suggestions: lifestyle scenes relevant to {config['market_name']} culture
• Keywords: mix of {config['language']} market search terms

FEATURES SECTION FOR {config['market_name']}:
• Feature callouts that resonate with {config['language']} consumers
• Benefits framed from {config['market_name']} perspective
• Technical specs presented in {config['market_name']} preferred format
• Comparison tables using {config['market_name']} competitive landscape

TRUST SECTION FOR {config['market_name']}:
• Trust builders relevant to {config['market_name']} market (certifications, guarantees)
• Social proof formats preferred in {config['market_name']}
• Customer testimonial styles for {config['language']} audience
• Return/warranty information per {config['market_name']} expectations

CULTURAL ADAPTATION FOR A+ CONTENT:
🎨 Visual Style: {config['market_name']} aesthetic preferences
🛍️ Shopping Behavior: {config['market_name']} purchase decision factors
📱 Device Usage: {config['market_name']} mobile vs desktop preferences
💬 Communication Style: {config['language']} formal/informal balance
🏆 Quality Indicators: What {config['market_name']} consumers value most

EXAMPLE A+ HERO FOR {config['market_name']}:
{{
  "section1_hero": {{
    "title": "Suggest titles that emphasize {cultural_elements[0] if cultural_elements else 'market relevance'}",
    "content": "Write content suggestions that highlight {power_words[0] if power_words else 'quality'} from {config['market_name']} consumer perspective",
    "keywords": ["Include", "{config['language']}", "market", "search", "terms"],
    "imageDescription": "Lifestyle image showing product use in {config['market_name']} cultural context",
    "seoOptimization": "Focus on {config['market_name']} market SEO and cultural relevance"
  }}
}}

MARKET-SPECIFIC A+ REQUIREMENTS:
• Hero images should show {config['market_name']} lifestyle contexts
• Feature callouts using {config['market_name']} preferred terminology
• Comparison charts with {config['market_name']} competitive products
• Trust elements valued in {config['market_name']} (certifications, reviews, guarantees)
• Call-to-action styles that work in {config['market_name']}

REMEMBER: Instructions in English, suggestions for {config['market_name']} market!
"""
        
        return aplus_enhancement