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
                
                # Native German copywriting rules - OPTIMIZED FOR 10/10 QUALITY
                "enforcement_rules": [
                    "🚨 CRITICAL: You MUST include German umlauts ä, ö, ü, ß in ALL appropriate words - NO EXCEPTIONS",
                    "UMLAUT EXAMPLES: für NOT fr, größer NOT grosser, Abkühlung NOT Abkuhlung, heißesten NOT heissesten, Oberfläche NOT Oberflache, Qualität NOT Qualitat, zuverlässig NOT zuverlas, müheloser NOT muhelos",
                    "COMMON UMLAUT WORDS: Größe, Höhe, Kühlung, Küche, hören, fühlen, natürlich, schön, größer, wärmer, kälter, Wärme",
                    "🔥 EMOTIONAL HOOK FORMULA - FIRST BULLET MUST START WITH:",
                    "Pattern: '[EMOTIONAL BENEFIT] wie ein Profi – ganz ohne [PROBLEM] oder [FRUSTRATION].'",
                    "Examples: 'Hygienisch schneiden wie ein Profi – ganz ohne Geschmacksübertragung oder Küchenchaos.'",
                    "Examples: 'Endlich erfrischende Abkühlung wie ein Profi – ganz ohne schwere Geräte oder laute Ventilatoren.'",
                    "🔧 BULLET STRUCTURE OPTIMIZATION:",
                    "Split long bullets into 2 clear sentences: 1st = core benefit, 2nd = scenario/feature",
                    "Example: 'Erste kurze Benefit-Aussage mit Emotion. Zweite Aussage erklärt zusätzliche Features oder Anwendung.'",
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
                
                # Essential French words
                "essential_words": [
                    "le", "la", "les", "et", "avec", "pour", "de", "du", "des", "est",
                    "avoir", "être", "faire", "aller", "venir", "voir", "savoir", "très", "bien", "tout"
                ],
                
                # Sophisticated French power words for luxury market
                "power_words": [
                    "qualité", "élégant", "raffinement", "sophistiqué", "excellence", "luxueux",
                    "performance", "innovation", "fiabilité", "précision", "efficace", "distingué",
                    "supérieur", "exceptionnel", "pratique", "moderne", "prestigieux", "exclusif",
                    "artisanal", "français", "authentique", "noble", "délicat", "harmonieux"
                ],
                
                # French lifestyle and cultural elements
                "cultural_elements": [
                    "Enfin le confort à la française",
                    "L'élégance pratique du quotidien", 
                    "Savourer chaque moment de fraîcheur",
                    "Qualité française authentique",
                    "Raffinement discret et efficace",
                    "Art de vivre français moderne",
                    "Sophistication naturelle"
                ],
                
                # Natural French expressions
                "formality_words": [
                    "Savourez", "Découvrez", "Profitez de", "Laissez-vous séduire par",
                    "Offrez-vous", "Adoptez", "Choisissez l'excellence",
                    "Vivez l'expérience", "Ressentez la différence", "Appréciez le raffinement"
                ],
                
                # French copywriting rules - OPTIMIZED FOR 10/10 QUALITY
                "enforcement_rules": [
                    "🚨 CRITICAL: You MUST use proper French accents é, è, à, ç, ù, â, ê, î, ô, û in ALL words",
                    "ACCENT EXAMPLES: qualité NOT qualite, élégant NOT elegant, français NOT francais, très NOT tres, être NOT etre, première NOT premiere",
                    "MANDATORY ACCENTS: raffinement, précision, efficacité, sécurité, créé, conçu, développé, intégré",
                    "🔥 FRENCH SOPHISTICATION FORMULA - FIRST BULLET MUST START WITH:",
                    "PATTERN 1: '[BENEFIT RAFFINÉ] à la française – sans [INCONVÉNIENT] ni [PROBLÈME].' (Use ONLY in 1st bullet)",
                    "PATTERN 2: '[BENEFIT] avec [SOPHISTICATION] française pour [RÉSULTAT].' (2nd bullet)",
                    "PATTERN 3: '[DESIGN SUPÉRIEUR] qui garantit [PRATICITÉ RAFFINÉE] et assure [ÉLÉGANCE LUXUEUSE].' (3rd bullet - MUST include: supérieur + raffiné/raffinée + luxueux/luxueuse)",
                    "PATTERN 4: '[PERFORMANCE EXCEPTIONNELLE] avec [PRÉCISION FRANÇAISE] pour [EXPÉRIENCE PREMIUM].' (4th bullet)",
                    "PATTERN 5: '[CADEAU LUXUEUX]: [SOPHISTICATION] française idéale à [OCCASION] pour [BÉNÉFICIAIRE RAFFINÉ].' (5th bullet)",
                    "Examples: 'Rafraîchissement élégant à la française – sans bruit excessif ni consommation.'",
                    "Examples: 'Performance avec raffinement français pour un confort optimal.'",
                    "Examples: 'Design supérieur qui garantit praticité raffinée et assure élégance luxueuse.'",
                    "🔧 BULLET STRUCTURE OPTIMIZATION:",
                    "🚨 STRICT LENGTH REQUIREMENT: 180-230 characters maximum (NEVER exceed 230 chars for mobile scan-ability)",
                    "🔥 CRITICAL POWER WORDS: Each bullet MUST contain minimum 2-3 power words from:",
                    "excellence, qualité, raffinement, luxueux, premium, sophistiqué, français, élégant, supérieur, exceptionnel",
                    "STRUCTURE: 'Label + benefit + proof + application' in 180-250 chars",
                    "Split sophisticated bullets into 2-3 scannable sentences with French flair",
                    "Example: 'EXCELLENCE FRANÇAISE: Raffinement authentique pour confort optimal. Conception premium qui garantit satisfaction.'",
                    "BALANCE: 70% lifestyle sophistication, 30% technical specs",
                    "INCLUDE: 'Cadeau parfait pour la Saint-Valentin' or seasonal French elegance",
                    "WRITE sophisticated French - maintain refinement without being pretentious"
                ],
                
                "avoid_words": ["the", "and", "with", "for", "is", "quality", "professional"]
            },
            
            "it": {
                "market_name": "Italy",
                "marketplace": "it",
                "language": "Italian",
                "currency": "EUR", 
                "language_code": "it",
                
                # Essential Italian words
                "essential_words": [
                    "il", "la", "le", "gli", "e", "con", "per", "di", "da", "in", "è",
                    "avere", "essere", "fare", "andare", "venire", "vedere", "sapere", "molto", "bene", "tutto"
                ],
                
                # Sophisticated Italian power words for luxury market
                "power_words": [
                    "qualità", "eleganza", "stile", "raffinato", "bellezza", "lussuoso",
                    "prestazioni", "innovazione", "affidabilità", "precisione", "efficace", "distinto",
                    "superiore", "eccezionale", "pratico", "moderno", "prestigioso", "esclusivo",
                    "artigianale", "italiano", "autentico", "nobile", "delicato", "armonioso"
                ],
                
                # Italian lifestyle and cultural elements
                "cultural_elements": [
                    "Finalmente il comfort all'italiana",
                    "L'eleganza pratica del quotidiano", 
                    "Assaporare ogni momento di freschezza",
                    "Qualità italiana autentica",
                    "Raffinatezza discreta ed efficace",
                    "Arte di vivere italiana moderna",
                    "Sofisticazione naturale"
                ],
                
                # Natural Italian expressions
                "formality_words": [
                    "Assaporate", "Scoprite", "Godetevi", "Lasciatevi conquistare da",
                    "Concedetevi", "Adottate", "Scegliete l'eccellenza",
                    "Vivete l'esperienza", "Sentite la differenza", "Apprezzate la raffinatezza"
                ],
                
                # Italian copywriting rules - OPTIMIZED FOR 10/10 QUALITY
                "enforcement_rules": [
                    "🚨 CRITICAL: You MUST use proper Italian accents à, è, é, ì, í, ò, ó, ù, ú in ALL words",
                    "ACCENT EXAMPLES: qualità NOT qualita, è NOT e, più NOT piu, perché NOT perche, città NOT citta",
                    "MANDATORY ACCENTS: funzionalità, comodità, sicurezza, efficacità, creato, progettato, sviluppato, integrato",
                    "🔥 ITALIAN SOPHISTICATION FORMULA - VARIED PATTERNS:",
                    "PATTERN 1: '[BENEFIT RAFFINATO] all'italiana – senza [INCONVENIENTE] né [PROBLEMA]. Dimensioni: 18x9x22cm.' (1st bullet)",
                    "PATTERN 2: '[SOFISTICAZIONE] italiana con [PRESTAZIONI] per [RISULTATO]. Lavabile in lavastoviglie.' (2nd bullet)",
                    "PATTERN 3: '[INNOVAZIONE] che unisce [PRATICITÀ] e [ELEGANZA]. Materiali premium certificati.' (3rd bullet - vary from pattern 1)",
                    "PATTERN 4: '[TECNOLOGIA] avanzata per [ESPERIENZA]. Autonomia 10 ore, ricarica USB-C.' (4th bullet - technical focus)",
                    "PATTERN 5: '[REGALO PERFETTO]: Design italiano per [OCCASIONE]. Garanzia 24 mesi inclusa.' (5th bullet)",
                    "Examples: 'Raffreddamento elegante all'italiana – senza rumore eccessivo né consumo inutile. Dimensioni compatte 18x9x22cm, lavabile in lavastoviglie.'",
                    "Examples: 'Prestazioni con raffinatezza italiana per un comfort ottimale. Autonomia 10 ore, peso 380g, facile da trasportare.'",
                    "Examples: 'Design superiore che garantisce praticità raffinata e assicura eleganza lussuosa. Materiali premium lavabili in lavastoviglie.'",
                    "🔧 BULLET STRUCTURE OPTIMIZATION:",
                    "🚨 CRITICAL REQUIREMENTS FOR EACH BULLET:",
                    "1. LENGTH: 180-210 characters (optimal for mobile scan-ability)",
                    "2. POWER WORDS: EACH bullet MUST include 2-3 of: eccellenza, qualità, raffinatezza, lussuoso, premium, sofisticato, italiano, elegante, superiore, eccezionale",
                    "3. ITALIAN SOPHISTICATION: EACH bullet MUST mention italiano/italiana/raffinato/elegante",
                    "4. SPECIFICATIONS: Include dimensions (18x9x22cm), weight (380g), or 'lavabile in lavastoviglie' where relevant",
                    "STRUCTURE: 'Label + benefit + proof + application' in 180-230 chars",
                    "Split sophisticated bullets into 2-3 scannable sentences with Italian flair",
                    "Example: 'ECCELLENZA ITALIANA: Raffinatezza autentica per comfort ottimale. Concezione premium che garantisce soddisfazione.'",
                    "BALANCE: 70% lifestyle sophistication, 30% technical specs",
                    "INCLUDE: 'Regalo perfetto per San Valentino' or seasonal Italian elegance",
                    "WRITE sophisticated Italian - maintain refinement without being pretentious"
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
            
            "pl": {
                "market_name": "Poland",
                "marketplace": "pl", 
                "language": "Polish",
                "currency": "PLN",
                "language_code": "pl",
                
                # Essential Polish words
                "essential_words": [
                    "i", "w", "na", "z", "do", "że", "się", "nie", "to", "ale",
                    "być", "mieć", "móc", "jak", "czy", "który", "bardzo", "już"
                ],
                
                # Emotional power words for Polish consumers
                "power_words": [
                    "wreszcie", "idealny", "wygodny", "łatwy", "skuteczny", "niezawodny",
                    "wysokiej jakości", "praktyczny", "doskonały", "niezbędny", "wyjątkowy",
                    "komfortowy", "oszczędny", "profesjonalny", "trwały", "elegancki"
                ],
                
                # Polish lifestyle and emotional elements
                "cultural_elements": [
                    "Wreszcie bez bólu pleców i szyi", 
                    "Idealny do domu i biura",
                    "Doskonały prezent na każdą okazję",
                    "Więcej komfortu w codziennym życiu",
                    "Zaoszczędź czas i ciesz się życiem",
                    "Poczuj różnicę już dziś",
                    "Zainwestuj w swoją wygodę"
                ],
                
                # Natural Polish phrases
                "formality_words": [
                    "Ciesz się", "Doświadcz", "Odkryj", "Skorzystaj z",
                    "Pozwól sobie na", "Wypróbuj", "Zainwestuj w",
                    "Poczuj różnicę", "Zyskaj więcej", "Zadbaj o siebie"
                ],
                
                # Polish copywriting rules
                "enforcement_rules": [
                    "🚨 CRITICAL: Use proper Polish characters ą, ć, ę, ł, ń, ó, ś, ź, ż in ALL words",
                    "Examples: więcej NOT wiecej, łatwy NOT latwy, jakość NOT jakosc, już NOT juz",
                    "WRITE emotional hooks: 'Wreszcie bez [PROBLEM]' or 'Ciesz się [BENEFIT]'", 
                    "USE Polish power words: wreszcie, idealny, wygodny, łatwy, doskonały",
                    "BALANCE: 60% lifestyle benefits, 40% technical specs",
                    "INCLUDE: 'Idealny prezent na Boże Narodzenie' or gift angles",
                    "WRITE warm, conversational Polish - avoid overly formal language"
                ],
                
                "avoid_words": ["the", "and", "with", "for", "is", "quality", "professional"]
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
        elif marketplace == "pl" or language == "pl":
            market_code = "pl"
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

{'📌 GERMAN BULLET POINTS - 10/10 QUALITY STRUCTURE:' if market_code == 'de' else f'BULLETS FOR {config["language"].upper()}:'}
• {'1st BULLET = EMOTIONAL HOOK: "[BENEFIT] wie ein Profi – ganz ohne [PROBLEM]."' if market_code == 'de' else f'Each bullet in {config["language"]}'}
• {'2nd BULLET: 2-3 scannable sentences. Hook + feature + application. Mobile-optimized.' if market_code == 'de' else 'Start with benefits'}
• {'3rd BULLET: 2-3 digestible sentences. Technical detail + lifestyle benefit + scenario.' if market_code == 'de' else 'Include cultural elements'}
• {'4th BULLET: Gift/seasonal angle in 2-3 readable sentences with emotional appeal.' if market_code == 'de' else 'Natural native expressions'}
• {'5th BULLET: Trust/guarantee in 2-3 substantial but scannable sentences.' if market_code == 'de' else 'Trust elements'}

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

{'🔥 GERMAN 10/10 BULLET OPTIMIZATION WITH BRAND TONE LABELS 🔥' if market_code == 'de' else ''}
{'CRITICAL: Include German brand tone labels (translate from English) + emotional hooks:' if market_code == 'de' else ''}
{'• "PROFESSIONELLE LEISTUNG: Erfrischende Abkühlung wie ein Profi – ganz ohne schwere Geräte."' if market_code == 'de' else ''}
{'• "BEWÄHRTE QUALITÄT: Hygienisch schneiden wie ein Profi – ganz ohne Geschmacksübertragung."' if market_code == 'de' else ''}
{'• "ZERTIFIZIERTE KÜHLUNG: Perfekte Abkühlung wie ein Profi – ganz ohne teure Klimaanlage."' if market_code == 'de' else ''}
{'MANDATORY: Each bullet MUST start with German brand tone label + emotional hook formula' if market_code == 'de' else ''}

{'🔥 FRENCH 10/10 BULLET OPTIMIZATION WITH SOPHISTICATED LABELS 🔥' if market_code == 'fr' else ''}
{'CRITICAL: Include French brand tone labels with sophisticated elegance + French hooks:' if market_code == 'fr' else ''}
{'• "EXCELLENCE FRANÇAISE: Rafraîchissement élégant à la française – sans bruit excessif ni consommation." (PATTERN 1 - Use ONLY once)' if market_code == 'fr' else ''}
{'• "QUALITÉ SUPÉRIEURE: Performance avec raffinement français pour un confort optimal et une satisfaction durable." (PATTERN 2)' if market_code == 'fr' else ''}
{'• "RAFFINEMENT MODERNE: Design innovant qui garantit praticité élégante et assure distinction quotidienne." (PATTERN 3)' if market_code == 'fr' else ''}
{'MANDATORY: Each bullet MUST start with French brand tone label + "à la française" sophistication formula' if market_code == 'fr' else ''}
{'' if market_code == 'fr' else ''}
{'BULLET STRUCTURE - FRENCH SOPHISTICATION OPTIMIZED (2-3 SENTENCES):' if market_code == 'fr' else ''}
{'✅ Sentence 1: Sophisticated benefit with French flair (15-20 words)' if market_code == 'fr' else ''}
{'✅ Sentence 2: Elegant technical detail (12-18 words)' if market_code == 'fr' else ''}
{'✅ Sentence 3 (optional): Refined application/lifestyle (10-15 words)' if market_code == 'fr' else ''}
{'📱 FRENCH MOBILE: Each sentence sophisticated yet scannable, refined but accessible' if market_code == 'fr' else ''}
{'❌ AVOID: Overly pretentious language OR casual American-style copy' if market_code == 'fr' else ''}
{'' if market_code == 'fr' else ''}
{'FRENCH ACCENT PERFECTION CHECKLIST:' if market_code == 'fr' else ''}
{'✅ qualité (not qualite), élégant (not elegant), précision (not precision), efficacité (not efficacite)' if market_code == 'fr' else ''}
{'✅ français (not francais), être (not etre), première (not premiere), créé (not cree), développé (not developpe)' if market_code == 'fr' else ''}
{'✅ raffinement (not raffinement), intégré (not integre), sécurité (not securite), conçu (not concu)' if market_code == 'fr' else ''}
{'' if market_code == 'de' else ''}
{'BULLET STRUCTURE - MOBILE SCAN-ABILITY OPTIMIZED (2-3 SENTENCES):' if market_code == 'de' else ''}
{'✅ Sentence 1: Emotional hook/core benefit (15-20 words)' if market_code == 'de' else ''}
{'✅ Sentence 2: Key feature/technical detail (12-18 words)' if market_code == 'de' else ''}
{'✅ Sentence 3 (optional): Scenario/application (10-15 words)' if market_code == 'de' else ''}
{'📱 MOBILE-FIRST: Each sentence standalone readable, scannable, substantial but digestible' if market_code == 'de' else ''}
{'❌ AVOID: 50+ word single sentences OR overly short 5-word fragments' if market_code == 'de' else ''}
{'' if market_code == 'de' else ''}
{'UMLAUT PERFECTION CHECKLIST:' if market_code == 'de' else ''}
{'✅ für (not fr), größer (not grosser), Kühlung (not Kuhlung), Qualität (not Qualitat)' if market_code == 'de' else ''}
{'✅ müheloser (not muheloser), hören (not horen), schön (not schon), natürlich (not naturlich)' if market_code == 'de' else ''}
{'✅ Oberfläche (not Oberflache), wärmer (not warmer), Wärme (not Warme), Größe (not Grosse)' if market_code == 'de' else ''}

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
        elif marketplace == "pl" or language == "pl":
            market_code = "pl"
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