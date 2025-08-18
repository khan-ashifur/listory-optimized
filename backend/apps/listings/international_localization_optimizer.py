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
            
            "jp": {
                "market_name": "Japan",
                "marketplace": "jp", 
                "language": "Japanese",
                "currency": "JPY",
                "language_code": "ja",
                
                # Essential Japanese particles and words
                "essential_words": [
                    "は", "が", "を", "に", "で", "と", "の", "か", "も", "から",
                    "まで", "という", "として", "について", "によって", "ため", "こと", "もの"
                ],
                
                # Japanese emotional power words that drive conversions
                "power_words": [
                    "最高", "究極", "革命的", "画期的", "完璧", "高品質", "プレミアム", "特別",
                    "安心", "信頼", "快適", "便利", "簡単", "効果的", "優秀", "人気",
                    "おすすめ", "話題", "注目", "限定", "独占", "新登場", "進化", "改良"
                ],
                
                # Japanese lifestyle and cultural elements
                "cultural_elements": [
                    "日本の皆様に安心してお使いいただける",
                    "毎日の生活をより快適に",
                    "お客様の満足度を最優先に",
                    "品質へのこだわり",
                    "使いやすさを追求",
                    "安全・安心の日本品質",
                    "おもてなしの心で"
                ],
                
                # Polite Japanese expressions (very important for Japan market)
                "formality_words": [
                    "いただけます", "させていただき", "お客様", "皆様", "ございます",
                    "いたします", "させていただきます", "お使いください", "ご利用ください",
                    "ご安心ください", "お楽しみください", "ご体験ください"
                ],
                
                # Japanese copywriting rules - OPTIMIZED FOR 10/10 QUALITY
                "enforcement_rules": [
                    "🚨 CRITICAL: You MUST use proper Japanese characters: Hiragana (ひらがな), Katakana (カタカナ), and Kanji (漢字)",
                    "CHARACTER EXAMPLES: 高品質 NOT koushitsu, 安心 NOT anshin, 快適 NOT kaiteki, 便利 NOT benri",
                    "MANDATORY JAPANESE: すべて, について, として, による, ため, こと, もの, という",
                    "🔥 JAPANESE PERSUASION FORMULA - STRUCTURED APPROACH:",
                    "PATTERN 1: '【特徴】で【ベネフィット】を実現。お客様の【問題解決】をサポートします。' (1st bullet)",
                    "PATTERN 2: '【高品質素材】により【信頼性】を確保。毎日の【使用場面】で安心してご利用いただけます。' (2nd bullet)",
                    "PATTERN 3: '【独自技術】が【効果】を最大化。【具体的数値】で実証された性能をお届けします。' (3rd bullet)",
                    "PATTERN 4: '【簡単操作】で【時短効果】を実現。忙しい【ターゲット】の方にもおすすめです。' (4th bullet)",
                    "PATTERN 5: '【ギフト提案】：大切な方への【機会】のプレゼントとして最適です。' (5th bullet)",
                    "Examples: '【革新的ノイズキャンセリング】で集中できる環境を実現。お客様の生産性向上をサポートします。'",
                    "Examples: '【高品質ドライバー】により音質の信頼性を確保。毎日の通勤・作業で安心してご利用いただけます。'",
                    "🔧 BULLET STRUCTURE OPTIMIZATION:",
                    "🚨 LENGTH REQUIREMENT: 80-120 characters (optimal for Japanese mobile display)",
                    "🔥 POLITENESS LEVEL: MUST use 丁寧語 (polite form) - です/ます ending for all sentences",
                    "STRUCTURE: '【ラベル】+ 特徴説明 + お客様への価値提案' in 80-120 chars",
                    "MANDATORY ELEMENTS: Each bullet must include お客様/皆様 (honorific for customers)",
                    "GIFT INTEGRATION: Include appropriate Japanese gift occasions (お歳暮, お中元, etc.)",
                    "SAFETY EMPHASIS: Japanese customers highly value 安心・安全 (safety/security)",
                    "QUALITY FOCUS: Emphasize 品質管理, 検査済み, 保証付き (quality control, tested, guaranteed)",
                    "WRITE respectful, customer-first Japanese that builds trust and confidence"
                ],
                
                "avoid_words": ["cheap", "discount", "sale", "promotion"]  # Japanese prefer value over discount messaging
            },
            
            "ae": {
                "market_name": "United Arab Emirates",
                "marketplace": "ae",
                "language": "Arabic",
                "currency": "AED",
                "language_code": "ar",
                
                # Essential Arabic words and phrases
                "essential_words": [
                    "في", "من", "إلى", "على", "مع", "هذا", "هذه", "التي", "الذي", "كل", "أو", "إذا",
                    "عند", "بين", "أمام", "خلف", "تحت", "فوق", "داخل", "خارج", "ضد", "بدون"
                ],
                
                # Arabic emotional power words that drive conversions
                "power_words": [
                    "الأفضل", "ممتاز", "فاخر", "رائع", "مذهل", "استثنائي", "متقدم", "عالي الجودة",
                    "موثوق", "آمن", "مريح", "سهل", "فعال", "قوي", "متين", "عملي",
                    "حصري", "محدود", "جديد", "محسن", "مطور", "مبتكر", "عصري", "أنيق"
                ],
                
                # UAE lifestyle and cultural elements
                "cultural_elements": [
                    "مناسب للمنزل والمكتب الإماراتي",
                    "يناسب الأجواء الحارة في دولة الإمارات",
                    "مصمم خصيصاً لنمط الحياة الخليجي",
                    "يواكب التطور والحداثة في الإمارات",
                    "مثالي للعائلات الإماراتية",
                    "يلبي معايير الجودة العالمية",
                    "موافق للمعايير الإسلامية"
                ],
                
                # Formal Arabic expressions for business
                "formality_words": [
                    "بإمكانكم", "يسعدنا", "نفخر بتقديم", "نضمن لكم", "نوفر لكم",
                    "يشرفنا", "نقدم لكم", "نحرص على", "نهتم بـ", "نسعى لتوفير",
                    "بفضل", "من خلال", "بواسطة", "عبر استخدام", "لضمان"
                ],
                
                # Arabic copywriting rules - OPTIMIZED FOR UAE MARKET
                "enforcement_rules": [
                    "🚨 CRITICAL: You MUST use proper Arabic script with correct diacritics when necessary",
                    "ARABIC EXAMPLES: الجودة العالية NOT al-jawda al-alia, منتج ممتاز NOT montaj momtaz",
                    "MANDATORY ARABIC: جميع, حول, كـ, من خلال, لأجل, شيء, بواسطة",
                    "🔥 ARABIC PERSUASION FORMULA - UAE MARKET APPROACH:",
                    "PATTERN 1: '[الميزة الرئيسية] توفر [الفائدة المباشرة] لتحقيق [النتيجة المرغوبة] في منزلكم.' (1st bullet)",
                    "PATTERN 2: '[التقنية المتطورة] تضمن [الأداء الفائق] مع [الموثوقية العالية] للاستخدام اليومي.' (2nd bullet)",
                    "PATTERN 3: '[التصميم الأنيق] يجمع بين [الوظائف العملية] و[الجمال البصري] المناسب للمنازل الحديثة.' (3rd bullet)",
                    "PATTERN 4: '[سهولة الاستخدام] مع [التحكم الذكي] يجعل [المهمة اليومية] أسرع وأكثر راحة.' (4th bullet)",
                    "PATTERN 5: '[هدية مثالية] لمناسبة [عيد الفطر/عيد الأضحى/رمضان] للأهل والأحباب.' (5th bullet)",
                    "Examples: 'التقنية المتقدمة توفر أداءً استثنائياً لتحقيق الراحة المطلقة في منزلكم.'",
                    "Examples: 'النظام الذكي يضمن الفعالية العالية مع الموثوقية التامة للاستخدام اليومي.'",
                    "🔧 BULLET STRUCTURE FOR UAE:",
                    "🚨 RESPECT RTL (Right-to-Left) reading pattern in Arabic",
                    "🔥 CULTURAL CONSIDERATIONS: Include family values, hospitality, luxury lifestyle",
                    "LENGTH: 150-200 characters per bullet (Arabic is more compact)",
                    "POWER WORDS: Each bullet MUST contain 2-3 from: ممتاز, فاخر, موثوق, عملي, أنيق, متطور",
                    "RELIGIOUS SENSITIVITY: Use appropriate Islamic greetings and expressions when relevant",
                    "FAMILY FOCUS: Emphasize family benefits and household harmony",
                    "🇦🇪 UAE LUXURY MARKET: Include premium positioning and quality emphasis"
                ],
                
                "avoid_words": ["cheap", "basic", "simple", "ordinary"]  # UAE market prefers premium positioning
            },
            
            "mx": {
                "market_name": "Mexico",
                "marketplace": "mx",
                "language": "Mexican Spanish",
                "currency": "MXN",
                "language_code": "es-mx",
                
                # Essential Mexican Spanish words and expressions
                "essential_words": [
                    "el", "la", "los", "las", "de", "del", "para", "por", "con", "en", "que", "es", "muy", "más",
                    "pero", "como", "esta", "este", "todo", "todos", "bien", "mejor", "nuevo", "gran", "grande"
                ],
                
                # Mexican emotional power words that drive conversions
                "power_words": [
                    "increíble", "excelente", "extraordinario", "fantástico", "maravilloso", "perfecto", "único",
                    "premium", "de lujo", "súper", "genial", "padrísimo", "chévere", "bárbaro", "fabuloso",
                    "revolucionario", "innovador", "avanzado", "profesional", "confiable", "garantizado", 
                    "auténtico", "original", "mexicano", "tradicional", "moderno", "eficaz", "potente"
                ],
                
                # Mexican lifestyle and cultural elements
                "cultural_elements": [
                    "perfecto para la familia mexicana",
                    "ideal para fiestas y reuniones familiares",
                    "diseñado para el hogar mexicano",
                    "resistente al clima mexicano",
                    "con el sabor que nos gusta a los mexicanos",
                    "para disfrutar en grande como nos gusta",
                    "tradición y modernidad en uno solo",
                    "hecho pensando en México"
                ],
                
                # Mexican Spanish expressions and formality
                "formality_words": [
                    "le ofrecemos", "le garantizamos", "nos da mucho gusto", "es un honor",
                    "con mucho orgullo", "le aseguramos", "puede estar seguro", "sin duda alguna",
                    "definitivamente", "por supuesto", "desde luego", "claro que sí", "¡cómo no!"
                ],
                
                # Mexican copywriting rules - OPTIMIZED FOR 10/10 QUALITY
                "enforcement_rules": [
                    "🚨 CRITICAL: You MUST use Mexican Spanish with proper accent marks: á, é, í, ó, ú, ñ",
                    "MEXICAN EXAMPLES: México NOT Mexico, más NOT mas, años NOT anos, niños NOT ninos",
                    "MANDATORY ACCENTS: también, además, después, fácil, rápido, único, práctico, cómodo",
                    "🔥 MEXICAN PERSUASION FORMULA - CULTURAL APPROACH:",
                    "PATTERN 1: '¡[BENEFICIO INCREÍBLE] que va a cambiar tu [VIDA/HOGAR]! Le garantizamos [RESULTADO] sin [PROBLEMA].' (1st bullet - MUST use 'le garantizamos')",
                    "PATTERN 2: '[CARACTERÍSTICA PREMIUM] con tecnología mexicana para [RESULTADO GARANTIZADO]. Le ofrecemos calidad superior.' (2nd bullet - MUST use 'le ofrecemos')",
                    "PATTERN 3: '[DISEÑO INTELIGENTE] que combina tradición mexicana con innovación. Con mucho orgullo [BENEFICIO].' (3rd bullet - MUST use 'con mucho orgullo')",
                    "PATTERN 4: '[FACILIDAD TOTAL] para familias mexicanas. Puede estar seguro de [EXPERIENCIA SUPERIOR].' (4th bullet - MUST use 'puede estar seguro')",
                    "PATTERN 5: '[REGALO PERFECTO] para [DÍA DE MUERTOS/NAVIDAD]. Sin duda alguna, toda la familia va a amar [PRODUCTO].' (5th bullet - MUST use 'sin duda alguna')",
                    "Examples: '¡Rendimiento increíble que va a cambiar tu cocina! Sin ruido excesivo ni consumo alto.'",
                    "Examples: 'Tecnología premium con diseño avanzado para resultados garantizados todos los días.'",
                    "🔧 BULLET STRUCTURE FOR MEXICO:",
                    "🚨 MANDATORY MEXICAN FORMALITY: Each bullet MUST include ONE of: 'le garantizamos', 'le ofrecemos', 'con mucho orgullo', 'puede estar seguro', 'sin duda alguna'",
                    "🚨 MANDATORY MEXICAN WORDS: MUST use 'México', 'mexicana/mexicano', 'familia mexicana', 'tradición mexicana' at least 3 times total",
                    "🚨 USE EXCITEMENT: Mexican market responds to enthusiasm and energy - USE ¡ and ! frequently",
                    "🔥 FAMILY EMPHASIS: Always consider family benefits and gatherings - mention 'familia' in every bullet",
                    "LENGTH: 180-250 characters per bullet (Mexican Spanish is expressive)",
                    "POWER WORDS: Each bullet MUST contain 2-3 from: increíble, excelente, perfecto, garantizado, premium, súper, padrísimo, fantástico",
                    "CULTURAL WARMTH: Use warm, friendly tone that resonates with Mexican hospitality",
                    "CELEBRATION FOCUS: Include references to Mexican celebrations and traditions",
                    "🇲🇽 MEXICAN PRIDE: Reference Mexican quality, tradition, or family values in EVERY bullet",
                    "GUARANTEE EMPHASIS: Mexicans value security and guarantees - emphasize warranties and support",
                    "🔥 MANDATORY QUALITY SCORE BOOST: Use 'auténtico', 'original', 'tradicional', 'artesanal' to reach 10/10"
                ],
                
                "avoid_words": ["barato", "básico", "simple", "ordinario"]  # Mexican market values quality and style
            },
            
            "in": {
                "market_name": "India",
                "marketplace": "in",
                "language": "Indian English",
                "currency": "INR",
                "language_code": "en-in",
                
                # Essential Indian English words and expressions
                "essential_words": [
                    "the", "and", "for", "with", "from", "this", "that", "all", "best", "good", "great", "new", "quality",
                    "premium", "perfect", "ideal", "amazing", "excellent", "superior", "outstanding", "wonderful", "fantastic"
                ],
                
                # Indian emotional power words that drive conversions
                "power_words": [
                    "incredible", "amazing", "extraordinary", "fantastic", "wonderful", "perfect", "unique",
                    "premium", "luxury", "super", "great", "brilliant", "awesome", "fabulous", "spectacular",
                    "revolutionary", "innovative", "advanced", "professional", "reliable", "guaranteed", 
                    "authentic", "original", "indian", "traditional", "modern", "effective", "powerful",
                    "exclusive", "pioneering", "limited", "special", "unique", "superior", "elite", 
                    "unmatched", "top", "leading", "first", "leader", "masterpiece", "incredible"
                ],
                
                # Indian lifestyle and cultural elements
                "cultural_elements": [
                    "perfect for Indian families",
                    "ideal for festivals and family gatherings",
                    "designed for Indian homes",
                    "suitable for Indian climate",
                    "with the taste Indians love",
                    "to enjoy in grand style as we love",
                    "tradition and modernity combined",
                    "made with India in mind"
                ],
                
                # Indian English expressions and formality
                "formality_words": [
                    "we offer you", "we guarantee you", "it gives us great pleasure", "it is an honor",
                    "with great pride", "we assure you", "you can be sure", "without any doubt",
                    "definitely", "of course", "certainly", "absolutely", "no doubt about it!"
                ],
                
                # Indian copywriting rules - OPTIMIZED FOR 10/10 QUALITY
                "enforcement_rules": [
                    "🚨 CRITICAL: You MUST use Indian English with proper spellings: colour, flavour, honour, favourite",
                    "INDIAN EXAMPLES: colour NOT color, favourite NOT favorite, realise NOT realize, centre NOT center",
                    "MANDATORY SPELLINGS: organised, recognised, categorised, specialised, customised",
                    "🔥 INDIAN PERSUASION FORMULA - CULTURAL APPROACH:",
                    "PATTERN 1: 'INCREDIBLE [BENEFIT] that will transform your [LIFE/HOME]! We guarantee you [RESULT] without [PROBLEM].' (1st bullet - MUST use 'we guarantee you')",
                    "PATTERN 2: '[PREMIUM FEATURE] with Indian technology for [GUARANTEED RESULT]. We offer you superior quality.' (2nd bullet - MUST use 'we offer you')",
                    "PATTERN 3: '[INTELLIGENT DESIGN] that combines Indian tradition with innovation. With great pride [BENEFIT].' (3rd bullet - MUST use 'with great pride')",
                    "PATTERN 4: '[TOTAL CONVENIENCE] for Indian families. You can be sure of [SUPERIOR EXPERIENCE].' (4th bullet - MUST use 'you can be sure')",
                    "PATTERN 5: '[FESTIVAL READY] perfect for Diwali celebrations! Definitely the [BEST CHOICE] for your family.' (5th bullet - MUST use 'definitely')",
                    "🚨 USE ENTHUSIASM: Indian market responds to celebration and family focus - USE excitement frequently",
                    "🔥 FAMILY EMPHASIS: Always consider joint family benefits and gatherings - mention 'family' in every bullet",
                    "LENGTH: 180-250 characters per bullet (Indian English is expressive)",
                    "POWER WORDS: Each bullet MUST contain 2-3 from: incredible, amazing, perfect, guaranteed, premium, super, brilliant, fantastic",
                    "CULTURAL WARMTH: Use warm, respectful tone that resonates with Indian hospitality and values",
                    "FESTIVAL FOCUS: Include references to Indian festivals and celebrations",
                    "🇮🇳 INDIAN PRIDE: Reference Indian quality, tradition, or family values in EVERY bullet",
                    "GUARANTEE EMPHASIS: Indians value trust and guarantees - emphasize warranties and support",
                    "🔥 MANDATORY QUALITY SCORE BOOST: Use 'authentic', 'original', 'traditional', 'handcrafted' to reach 10/10"
                ],
                
                "avoid_words": ["cheap", "basic", "simple", "ordinary"]  # Indian market values quality and family benefits
            },
            
            "sa": {
                "market_name": "Saudi Arabia",
                "marketplace": "sa",
                "language": "Arabic",
                "currency": "SAR",
                "language_code": "ar-sa",
                
                # Essential Arabic words and expressions
                "essential_words": [
                    "في", "من", "إلى", "على", "مع", "عن", "كل", "هذا", "هذه", "ذلك", "تلك", "التي", "الذي", "جميع",
                    "أفضل", "جديد", "كبير", "صغير", "طويل", "قصير", "سريع", "بطيء", "جيد", "سيء", "كثير", "قليل"
                ],
                
                # Saudi Arabic emotional power words that drive conversions
                "power_words": [
                    "رائع", "ممتاز", "استثنائي", "فانتاستيك", "رائع", "مثالي", "فريد",
                    "بريميوم", "فاخر", "سوبر", "رائع", "رائع", "مذهل", "لذيذ", "منقطع النظير",
                    "ثوري", "مبتكر", "متقدم", "مهني", "موثوق", "مضمون", 
                    "أصلي", "حقيقي", "سعودي", "تقليدي", "حديث", "فعال", "قوي",
                    "حصري", "رائد", "محدود", "خاص", "فريد", "متفوق", "نخبة", 
                    "منقطع النظير", "قمة", "في المقدمة", "الأول", "قائد", "تحفة", "رائع"
                ],
                
                # Saudi lifestyle and cultural elements
                "cultural_elements": [
                    "مثالي للعائلة السعودية",
                    "مناسب للأعياد والتجمعات العائلية",
                    "مصمم للمنزل السعودي",
                    "مقاوم للمناخ السعودي",
                    "بالطعم الذي يحبه السعوديون",
                    "للاستمتاع بشكل كبير كما نحب",
                    "تراث وحداثة في واحد",
                    "مصنوع مع التفكير في السعودية"
                ],
                
                # Saudi Arabic expressions and formality
                "formality_words": [
                    "نقدم لكم", "نضمن لكم", "يسعدنا كثيراً", "إنه لشرف",
                    "بكل فخر", "نؤكد لكم", "يمكنكم التأكد", "بلا شك",
                    "بالتأكيد", "بالطبع", "طبعاً", "أكيد", "كيف لا!"
                ],
                
                # Saudi copywriting rules - EXACT MEXICO PATTERN FOR 10/10 QUALITY
                "enforcement_rules": [
                    "🚨 CRITICAL: You MUST use Saudi Arabic with proper Arabic characters and diacritics",
                    "SAUDI EXAMPLES: السعودية NOT Saudi Arabia, أكثر NOT more, سنوات NOT years",
                    "MANDATORY DIACRITICS: أيضاً، بالإضافة، بعد ذلك، سهل، سريع، فريد، عملي، مريح",
                    "🔥 SAUDI PERSUASION FORMULA - CULTURAL APPROACH:",
                    "PATTERN 1: '[مخزون محدود] ¡[فائدة مذهلة] ستغير حياتكم/منزلكم! أكثر من 10,000 عائلة سعودية راضية، نضمن لكم [النتيجة] بدون [المشكلة].' (1st bullet - MUST use 'نضمن لكم' + social proof + urgency)",
                    "PATTERN 2: '[أفضل من المنافسين بـ %40] [ميزة بريميوم] بالتكنولوجيا السعودية لـ[النتيجة المضمونة]. نقدم لكم جودة فائقة، أو استرداد كامل للمال.' (2nd bullet - MUST use 'نقدم لكم' + competitive edge + risk reversal)",
                    "PATTERN 3: '[تصميم رائد] يجمع بين التراث السعودي والابتكار الحصري. بكل فخر [الفائدة]، ★★★★★ 4.8/5 رضا العملاء.' (3rd bullet - MUST use 'بكل فخر' + social proof)",
                    "PATTERN 4: '[سهولة فريدة] تصميم خاص للعائلات السعودية. يمكنكم التأكد من [التجربة الفائقة]، ضمان الإرجاع لمدة 30 يوماً.' (4th bullet - MUST use 'يمكنكم التأكد' + guarantee)",
                    "PATTERN 5: '[فرصة أخيرة للعام الجديد] [هدية مثالية] في المخزون المحدود! بلا شك، كل العائلة ستحب [المنتج]، اطلبوا اليوم واستمتعوا غداً.' (5th bullet - MUST use 'بلا شك' + urgency + CTA)",
                    "Examples: '¡أداء مذهل سيغير مطبخكم! بدون ضوضاء زائدة واستهلاك عالي.'",
                    "Examples: 'تكنولوجيا بريميوم مع تصميم متقدم لنتائج مضمونة كل يوم.'",
                    "🔧 BULLET STRUCTURE FOR SAUDI ARABIA:",
                    "🚨 MANDATORY SAUDI FORMALITY: Each bullet MUST include ONE of: 'نضمن لكم', 'نقدم لكم', 'بكل فخر', 'يمكنكم التأكد', 'بلا شك'",
                    "🚨 MANDATORY SAUDI WORDS: MUST use 'السعودية', 'سعودي', 'العائلة السعودية', 'التراث السعودي' at least 3 times total",
                    "🚨 USE EXCITEMENT: Saudi market responds to enthusiasm and energy - USE exclamation marks frequently",
                    "🔥 FAMILY EMPHASIS: Always consider family benefits and gatherings - mention 'عائلة' in every bullet",
                    "LENGTH: 180-250 characters per bullet (Arabic is expressive)",
                    "POWER WORDS: Each bullet MUST contain 2-3 from: رائع, ممتاز, مثالي, مضمون, بريميوم, سوبر, رائع, فانتاستيك",
                    "CULTURAL WARMTH: Use warm, friendly tone that resonates with Saudi hospitality",
                    "CELEBRATION FOCUS: Include references to Saudi celebrations and traditions",
                    "🇸🇦 SAUDI PRIDE: Reference Saudi quality, tradition, or family values in EVERY bullet",
                    "GUARANTEE EMPHASIS: Saudis value security and guarantees - emphasize warranties and support",
                    "🔥 MANDATORY QUALITY SCORE BOOST: Use 'أصلي', 'أصيل', 'تقليدي', 'حرفي' to reach 10/10"
                ],
                
                "avoid_words": ["رخيص", "أساسي", "بسيط", "عادي"]  # Saudi market values quality and luxury
            },
            
            "tr": {
                "market_name": "Turkey",
                "marketplace": "tr",
                "language": "Turkish",
                "currency": "TRY",
                "language_code": "tr",
                
                # Essential Turkish words and expressions (copied from Mexico pattern)
                "essential_words": [
                    "ve", "ile", "için", "den", "dan", "da", "de", "ki", "bu", "şu", "o",
                    "olan", "olarak", "bir", "çok", "daha", "en", "her", "tüm", "ama", "ancak", "çok", "daha"
                ],
                
                # Turkish emotional power words that drive conversions (ENHANCED FOR 95+ SCORE)
                "power_words": [
                    "inanılmaz", "mükemmel", "olağanüstü", "fantastik", "harika", "kusursuz", "eşsiz",
                    "premium", "lüks", "süper", "muhteşem", "harika", "fevkalade", "nefis", "benzersiz",
                    "devrimsel", "yenilikçi", "gelişmiş", "profesyonel", "güvenilir", "garantili", 
                    "orijinal", "gerçek", "türk", "geleneksel", "modern", "etkili", "güçlü",
                    "eksklüzif", "çığır açan", "sınırlı", "özel", "benzersiz", "üstün", "elite", 
                    "rakipsiz", "doruk", "zirvede", "birinci", "lider", "şaheser", "harika"
                ],
                
                # Turkish lifestyle and cultural elements (Mexico pattern)
                "cultural_elements": [
                    "Türk ailesi için mükemmel",
                    "festivaller ve aile toplantıları için ideal",
                    "Türk evi için tasarlanmış",
                    "Türk iklimine dayanıklı",
                    "Türklerin sevdiği lezzet gibi",
                    "büyük şekilde keyif almak için",
                    "gelenek ve modernlik bir arada",
                    "Türkiye düşünülerek yapılmış"
                ],
                
                # Turkish expressions and formality (Mexico pattern)
                "formality_words": [
                    "size sunuyoruz", "size garanti ediyoruz", "büyük bir memnuniyetle", "onur duyuyoruz",
                    "büyük bir gururla", "size temin ediyoruz", "emin olabilirsiniz", "hiç şüphesiz",
                    "kesinlikle", "tabii ki", "elbette", "tabii ki", "nasıl olmasın!"
                ],
                
                # Turkish copywriting rules - EXACT MEXICO PATTERN FOR 10/10 QUALITY
                "enforcement_rules": [
                    "🚨 CRITICAL: You MUST use Turkish with proper Turkish characters: ç, ğ, ı, ö, ş, ü",
                    "TURKISH EXAMPLES: Türkiye NOT Turkey, daha NOT daha, çok NOT cok, için NOT icin",
                    "MANDATORY ACCENTS: ayrıca, böylece, sonra, kolay, hızlı, eşsiz, pratik, rahat",
                    "🔥 TURKISH PERSUASION FORMULA - CULTURAL APPROACH:",
                    "PATTERN 1: '[SINIRLI STOK] ¡[İNANILMAZ FAYDA] hayatınızı/evinizi değiştirecek! 10,000+ memnun Türk ailesi, size [SONUÇ] [SORUN] olmadan garanti ediyoruz.' (1st bullet - MUST use 'size garanti ediyoruz' + social proof + urgency)",
                    "PATTERN 2: '[RAKIPLERDEN %40 ÜSTÜN] [PREMIUM ÖZELLİK] Türk teknolojisi ile [GARANTİLİ SONUÇ] için. Size üstün kalite sunuyoruz, memnun kalmazsanız tam para iadesi.' (2nd bullet - MUST use 'size sunuyoruz' + competitive edge + risk reversal)",
                    "PATTERN 3: '[ÇIĞIR AÇAN TASARIM] Türk geleneğini yenilikle birleştiren eksklüzif çözüm. Büyük bir gururla [FAYDA], ★★★★★ 4.8/5 müşteri memnuniyeti.' (3rd bullet - MUST use 'büyük bir gururla' + social proof)",
                    "PATTERN 4: '[BENZERSIZ KOLAYLIK] Türk aileleri için özel tasarım. [ÜSTÜN DENEYİM] konusunda emin olabilirsiniz, 30 gün iade garantisi.' (4th bullet - MUST use 'emin olabilirsiniz' + guarantee)",
                    "PATTERN 5: '[YENİ YIL SON FIRSAT] [MÜKEMMEL HEDİYE] sınırlı stokta! Hiç şüphesiz, tüm aile [ÜRÜN]ü sevecek, bugün sipariş verin yarın keyfini çıkarın.' (5th bullet - MUST use 'hiç şüphesiz' + urgency + CTA)",
                    "Examples: '¡İnanılmaz performans mutfağınızı değiştirecek! Aşırı gürültü ve yüksek tüketim olmadan.'",
                    "Examples: 'Premium teknoloji ile gelişmiş tasarım her gün garantili sonuçlar için.'",
                    "🔧 BULLET STRUCTURE FOR TURKEY:",
                    "🚨 MANDATORY TURKISH FORMALITY: Each bullet MUST include ONE of: 'size garanti ediyoruz', 'size sunuyoruz', 'büyük bir gururla', 'emin olabilirsiniz', 'hiç şüphesiz'",
                    "🚨 MANDATORY TURKISH WORDS: MUST use 'Türkiye', 'Türk', 'Türk ailesi', 'Türk geleneği' at least 3 times total",
                    "🚨 USE EXCITEMENT: Turkish market responds to enthusiasm and energy - USE exclamation marks frequently",
                    "🔥 FAMILY EMPHASIS: Always consider family benefits and gatherings - mention 'aile' in every bullet",
                    "LENGTH: 180-250 characters per bullet (Turkish is expressive)",
                    "POWER WORDS: Each bullet MUST contain 3-4 from: inanılmaz, mükemmel, kusursuz, garantili, premium, süper, muhteşem, fantastik, eksklüzif, çığır açan, sınırlı, benzersiz, rakipsiz",
                    "🚨 URGENCY MANDATORY: Include urgency in bullets 1 and 5: 'sınırlı stok', 'son fırsat', 'bugün sipariş verin'",
                    "🚨 SOCIAL PROOF MANDATORY: Include in bullets 1 and 3: '10,000+ memnun Türk ailesi', '★★★★★ 4.8/5 müşteri memnuniyeti'",
                    "🚨 COMPETITIVE EDGE: Include in bullet 2: 'rakiplerden %40 üstün', 'piyasada tek'",
                    "🚨 RISK REVERSAL: Include guarantees: '30 gün iade garantisi', 'memnun kalmazsanız tam para iadesi'",
                    "CULTURAL WARMTH: Use warm, friendly tone that resonates with Turkish hospitality",
                    "CELEBRATION FOCUS: Include references to Turkish celebrations and traditions",
                    "🇹🇷 TURKISH PRIDE: Reference Turkish quality, tradition, or family values in EVERY bullet",
                    "GUARANTEE EMPHASIS: Turks value security and guarantees - emphasize warranties and support",
                    "🔥 MANDATORY QUALITY SCORE BOOST: Use 'orijinal', 'gerçek', 'geleneksel', 'el yapımı' to reach 10/10",
                    "🚨 CONVERSION OPTIMIZATION: Include call-to-action in bullet 5: 'bugün sipariş verin yarın keyfini çıkarın'"
                ],
                
                "avoid_words": ["ucuz", "temel", "basit", "sıradan"]  # Turkish market values quality and style
            },
            
            "br": {
                "market_name": "Brazil",
                "marketplace": "br",
                "language": "Brazilian Portuguese",
                "currency": "BRL",
                "language_code": "pt-br",
                
                # Essential Brazilian Portuguese words and expressions
                "essential_words": [
                    "o", "a", "os", "as", "de", "do", "da", "para", "por", "com", "em", "que", "é", "muito", "mais",
                    "mas", "como", "esta", "este", "todo", "todos", "bem", "melhor", "novo", "grande", "ótimo"
                ],
                
                # Brazilian emotional power words that drive conversions
                "power_words": [
                    "incrível", "excelente", "extraordinário", "fantástico", "maravilhoso", "perfeito", "único",
                    "premium", "de luxo", "super", "demais", "top", "show", "bacana", "sensacional",
                    "revolucionário", "inovador", "avançado", "profissional", "confiável", "garantido",
                    "autêntico", "original", "brasileiro", "tradicional", "moderno", "eficaz", "potente"
                ],
                
                # Brazilian lifestyle and cultural elements
                "cultural_elements": [
                    "perfeito para a família brasileira",
                    "ideal para festas e reuniões familiares",
                    "feito pensando no brasileiro",
                    "resistente ao clima tropical brasileiro",
                    "com o jeitinho brasileiro que a gente ama",
                    "para curtir em grande estilo como gostamos",
                    "tradição e modernidade juntas",
                    "qualidade brasileira de primeira"
                ],
                
                # Brazilian Portuguese expressions and formality
                "formality_words": [
                    "oferecemos a você", "garantimos para você", "temos o prazer", "é uma honra",
                    "com muito orgulho", "pode ter certeza", "sem dúvida nenhuma", "com toda certeza",
                    "definitivamente", "é claro", "sem problema", "pode contar", "está garantido"
                ],
                
                # Brazilian copywriting rules - OPTIMIZED FOR 10/10 QUALITY
                "enforcement_rules": [
                    "🚨 CRITICAL: You MUST use Brazilian Portuguese with proper accent marks: á, â, à, é, ê, í, ó, ô, õ, ú, ç",
                    "BRAZILIAN EXAMPLES: São Paulo NOT Sao Paulo, coração NOT coracao, função NOT funcao, proteção NOT protecao",
                    "MANDATORY ACCENTS: também, além, após, fácil, rápido, único, prático, cômodo, proteção, função",
                    "🔥 BRAZILIAN PERSUASION FORMULA - CULTURAL APPROACH:",
                    "PATTERN 1: '[BENEFÍCIO INCRÍVEL] que vai transformar sua [VIDA/CASA]! Garantimos [RESULTADO] sem [PROBLEMA].' (1st bullet - MUST use 'garantimos')",
                    "PATTERN 2: '[CARACTERÍSTICA PREMIUM] com tecnologia brasileira para [RESULTADO GARANTIDO]. Oferecemos qualidade superior.' (2nd bullet - MUST use 'oferecemos')",
                    "PATTERN 3: '[DESIGN INTELIGENTE] que combina tradição brasileira com inovação. Com muito orgulho [BENEFÍCIO].' (3rd bullet - MUST use 'com muito orgulho')",
                    "PATTERN 4: '[FACILIDADE TOTAL] para famílias brasileiras. Pode ter certeza de [EXPERIÊNCIA SUPERIOR].' (4th bullet - MUST use 'pode ter certeza')",
                    "PATTERN 5: '[PRESENTE PERFEITO] para [CARNAVAL/NATAL/DIA DAS MÃES]. Sem dúvida nenhuma, toda família vai amar [PRODUTO].' (5th bullet - MUST use 'sem dúvida nenhuma')",
                    "Examples: 'Performance incrível que vai transformar sua cozinha! Garantimos resultado sem barulho excessivo.'",
                    "Examples: 'Tecnologia premium com design avançado para resultados garantidos todo dia.'",
                    "🔧 BULLET STRUCTURE FOR BRAZIL:",
                    "🚨 MANDATORY BRAZILIAN FORMALITY: Each bullet MUST include ONE of: 'garantimos', 'oferecemos', 'com muito orgulho', 'pode ter certeza', 'sem dúvida nenhuma'",
                    "🚨 MANDATORY BRAZILIAN WORDS: MUST use 'Brasil', 'brasileira/brasileiro', 'família brasileira', 'tradição brasileira' at least 3 times total",
                    "🚨 USE ENTHUSIASM: Brazilian market loves energy and positivity - USE exclamation marks frequently",
                    "🔥 FAMILY EMPHASIS: Always consider family benefits and gatherings - mention 'família' in every bullet",
                    "LENGTH: 180-250 characters per bullet (Brazilian Portuguese is expressive)",
                    "POWER WORDS: Each bullet MUST contain 2-3 from: incrível, excelente, perfeito, garantido, premium, super, show, sensacional",
                    "CULTURAL WARMTH: Use warm, friendly tone that resonates with Brazilian hospitality and joy",
                    "CELEBRATION FOCUS: Include references to Brazilian celebrations and traditions",
                    "🇧🇷 BRAZILIAN PRIDE: Reference Brazilian quality, tradition, or family values in EVERY bullet",
                    "GUARANTEE EMPHASIS: Brazilians value security and guarantees - emphasize warranties and support",
                    "🔥 MANDATORY QUALITY SCORE BOOST: Use 'autêntico', 'original', 'tradicional', 'artesanal' to reach 10/10"
                ],
                
                "avoid_words": ["barato", "básico", "simples", "comum"]  # Brazilian market values quality and style
            },
            
            "nl": {
                "market_name": "Netherlands",
                "marketplace": "nl",
                "language": "Dutch",
                "currency": "EUR",
                "language_code": "nl",
                
                # Essential Dutch words and expressions
                "essential_words": [
                    "de", "het", "een", "van", "is", "in", "en", "op", "te", "met", "voor", "aan", "dat", "die", "er",
                    "zijn", "hebben", "worden", "kunnen", "gaan", "maken", "zien", "goed", "groot", "nieuw", "veel"
                ],
                
                # Dutch emotional power words that drive conversions
                "power_words": [
                    "geweldig", "uitstekend", "fantastisch", "perfect", "uniek", "premium", "luxe", "super", "top",
                    "revolutionair", "innovatief", "geavanceerd", "professioneel", "betrouwbaar", "gegarandeerd",
                    "authentiek", "origineel", "nederlands", "traditioneel", "modern", "effectief", "krachtig",
                    "praktisch", "slim", "duurzaam", "kwaliteit", "comfort", "stijlvol", "elegant"
                ],
                
                # Dutch lifestyle and cultural elements
                "cultural_elements": [
                    "perfect voor het Nederlandse gezin",
                    "ideaal voor gezellige avonden en familiebijeenkomsten",
                    "gemaakt met het Nederlandse leven in gedachten",
                    "bestand tegen het Nederlandse klimaat",
                    "met de Nederlandse no-nonsense mentaliteit",
                    "voor die echte Nederlandse gezelligheid",
                    "traditie en moderniteit samen",
                    "Nederlandse kwaliteit en betrouwbaarheid"
                ],
                
                # Dutch expressions and formality (Direct but polite Dutch style)
                "formality_words": [
                    "wij garanderen u", "wij bieden u", "met trots presenteren wij", "u kunt er zeker van zijn",
                    "zonder twijfel", "absoluut zeker", "natuurlijk", "uiteraard", "zeker weten", "gegarandeerd",
                    "u verdient het beste", "wij zorgen ervoor", "vertrouw op onze kwaliteit"
                ],
                
                # Dutch copywriting rules - OPTIMIZED FOR 10/10 QUALITY
                "enforcement_rules": [
                    "🚨 CRITICAL: You MUST use proper Dutch grammar and spelling - no German or English mix-ups",
                    "DUTCH EXAMPLES: gezellig NOT gemutlich, fiets NOT bicycle, huis NOT haus, kwaliteit NOT qualitat",
                    "MANDATORY DUTCH WORDS: Use typical Dutch words like 'gezellig', 'lekker', 'fijn', 'handig', 'slim'",
                    "🔥 DUTCH PERSUASION FORMULA - NO-NONSENSE APPROACH:",
                    "PATTERN 1: '[GEWELDIG VOORDEEL] dat uw [LEVEN/HUIS] zal verbeteren! Wij garanderen [RESULTAAT] zonder [PROBLEEM].' (1st bullet - MUST use 'wij garanderen')",
                    "PATTERN 2: '[PREMIUM EIGENSCHAP] met Nederlandse kwaliteit voor [GEGARANDEERD RESULTAAT]. Wij bieden u superieure prestaties.' (2nd bullet - MUST use 'wij bieden u')",
                    "PATTERN 3: '[SLIM ONTWERP] dat Nederlandse prakticaliteit combineert met innovatie. Met trots presenteren wij [VOORDEEL].' (3rd bullet - MUST use 'met trots presenteren wij')",
                    "PATTERN 4: '[TOTALE GEMAK] voor Nederlandse gezinnen. U kunt er zeker van zijn dat u [SUPERIEURE ERVARING] krijgt.' (4th bullet - MUST use 'u kunt er zeker van zijn')",
                    "PATTERN 5: '[PERFECT CADEAU] voor [KONINGSDAG/SINTERKLAAS/KERST]. Zonder twijfel zal elk gezin genieten van [PRODUCT].' (5th bullet - MUST use 'zonder twijfel')",
                    "Examples: 'Geweldige prestaties die uw keuken zullen transformeren! Wij garanderen resultaten zonder overlast.'",
                    "Examples: 'Premium technologie met geavanceerd ontwerp voor gegarandeerde resultaten elke dag.'",
                    "🔧 BULLET STRUCTURE FOR NETHERLANDS:",
                    "🚨 MANDATORY DUTCH FORMALITY: Each bullet MUST include ONE of: 'wij garanderen', 'wij bieden u', 'met trots presenteren wij', 'u kunt er zeker van zijn', 'zonder twijfel'",
                    "🚨 MANDATORY DUTCH WORDS: MUST use 'Nederland', 'Nederlandse', 'gezin', 'gezellig' at least 3 times total",
                    "🚨 DUTCH DIRECTNESS: Dutch market appreciates direct, honest communication - be straightforward but friendly",
                    "🔥 FAMILY FOCUS: Dutch value family time and 'gezelligheid' - mention family benefits and togetherness",
                    "LENGTH: 160-220 characters per bullet (Dutch is more concise than other languages)",
                    "POWER WORDS: Each bullet MUST contain 2-3 from: geweldig, uitstekend, perfect, gegarandeerd, premium, super, fantastisch, slim",
                    "PRACTICAL BENEFITS: Dutch appreciate practical, functional benefits - emphasize utility and efficiency",
                    "QUALITY FOCUS: Include references to Dutch quality standards and reliability",
                    "🇳🇱 DUTCH PRIDE: Reference Dutch innovation, quality, or family values in EVERY bullet",
                    "SUSTAINABILITY: Dutch market increasingly values sustainability and environmental consciousness",
                    "🔥 MANDATORY QUALITY SCORE BOOST: Use 'authentiek', 'origineel', 'traditioneel', 'duurzaam' to reach 10/10"
                ],
                
                "avoid_words": ["goedkoop", "basis", "eenvoudig", "gewoon"]  # Dutch market values quality and innovation
            },
            
            "se": {
                "market_name": "Sweden", 
                "marketplace": "se",
                "language": "Swedish",
                "currency": "SEK",
                "language_code": "sv",
                
                # Essential Swedish words and expressions
                "essential_words": [
                    "och", "att", "det", "en", "som", "för", "på", "med", "av", "till", "är", "den", "ett", "i", "om",
                    "har", "de", "så", "man", "kan", "vara", "från", "eller", "när", "kommer", "ska", "göra", "mycket"
                ],
                
                # Swedish emotional power words that drive conversions
                "power_words": [
                    "fantastisk", "utmärkt", "enastående", "perfekt", "unik", "premium", "lyx", "super", "topp",
                    "revolutionerande", "innovativ", "avancerad", "professionell", "pålitlig", "garanterad",
                    "äkta", "original", "svensk", "traditionell", "modern", "effektiv", "kraftfull",
                    "praktisk", "smart", "hållbar", "kvalitet", "komfort", "stilfull", "elegant", "lagom"
                ],
                
                # Swedish lifestyle and cultural elements (lagom, hygge, sustainability)
                "cultural_elements": [
                    "perfekt för svenska hem med lagom-filosofi",
                    "idealisk för mys och svenska familjesammankomster", 
                    "anpassad efter svenskt liv och nordiska värderingar",
                    "byggd för svenskt klimat och förhållanden",
                    "med svensk enkelhet och funktionalitet i fokus",
                    "för äkta svensk mys och välbefinnande",
                    "kombinerar svensk tradition med modern innovation",
                    "svensk kvalitet som håller i generationer",
                    "perfekt för fika och svenska gemenskaper",
                    "hållbar design i linje med svenska miljövärden"
                ],
                
                # Swedish expressions and formality (Direct but warm Swedish style)
                "formality_words": [
                    "vi garanterar dig", "vi erbjuder dig", "med stolthet presenterar vi", "du kan vara säker på",
                    "utan tvekan", "absolut säkert", "naturligtvis", "självklart", "helt säkert", "garanterat",
                    "du förtjänar det bästa", "vi ser till att", "lita på vår kvalitet", "vi lovar dig"
                ],
                
                # Swedish copywriting rules - OPTIMIZED FOR 10/10 QUALITY  
                "enforcement_rules": [
                    "🚨 CRITICAL: You MUST use authentic Swedish language - no Norwegian or Danish mix-ups",
                    "SWEDISH EXAMPLES: kök NOT køkken, hus NOT huis, kvalitet NOT kvaliteetti, bra NOT bro",
                    "MANDATORY SWEDISH CONCEPTS: Include 'lagom' (perfect balance), 'mys' (coziness), 'hållbarhet' (sustainability)",
                    "🔥 SWEDISH PERSUASION FORMULA - LAGOM & FUNCTIONAL APPROACH:",
                    "PATTERN 1: '[FANTASTISK FÖRDEL] som kommer förbättra ditt [LIV/HEM] på ett lagom sätt! Vi garanterar [RESULTAT] utan [PROBLEM].' (1st bullet - MUST use 'vi garanterar')",
                    "PATTERN 2: '[PREMIUM EGENSKAPER] med svensk kvalitet för [GARANTERAT RESULTAT]. Vi erbjuder dig överlägsen prestanda.' (2nd bullet - MUST use 'vi erbjuder dig')",
                    "PATTERN 3: '[SMART DESIGN] som kombinerar svensk praktiskhet med innovation. Med stolthet presenterar vi [FÖRDEL].' (3rd bullet - MUST use 'med stolthet presenterar vi')",
                    "PATTERN 4: '[TOTAL BEKVÄMLIGHET] för svenska familjer som värdesätter lagom. Du kan vara säker på [ÖVERLÄGSEN UPPLEVELSE].' (4th bullet - MUST use 'du kan vara säker på')",
                    "PATTERN 5: '[PERFEKT PRESENT] för [MIDSOMMAR/LUCIA/JUL]. Utan tvekan kommer varje familj att uppskatta [PRODUKT].' (5th bullet - MUST use 'utan tvekan')",
                    "Examples: 'Fantastiska prestationer som kommer transformera ditt kök på lagom sätt! Vi garanterar resultat utan krångel.'",
                    "Examples: 'Premium teknologi med avancerad design för garanterade resultat varje dag.'",
                    "🇸🇪 SWEDISH CULTURAL FOCUS:",
                    "- Lagom philosophy emphasis (balanced, not too much, just right)",
                    "- Environmental consciousness and sustainability (miljötänk, hållbarhet)",
                    "- Quality and functionality over flashiness (kvalitet, funktionalitet)",
                    "- Mys and comfort references (mys, komfort, välbefinnande)", 
                    "- Swedish design principles (enkelhet, funktion, skönhet)",
                    "LAGOM FOCUS: Include balanced lifestyle references (lagom comfort, lagom quality)",
                    "SUSTAINABILITY FOCUS: Include environmental consciousness (hållbar, miljövänlig)",
                    "DESIGN FOCUS: Include Swedish design heritage (svensk design, nordisk stil)",
                    "🇸🇪 SWEDISH PRIDE: Reference Swedish quality, lagom balance, or sustainability in EVERY bullet",
                    "QUALITY EMPHASIS: Swedes value durability and function - emphasize long-term value and reliability",
                    "🔥 MANDATORY QUALITY SCORE BOOST: Use 'äkta', 'pålitlig', 'hållbar', 'lagom' to reach 10/10"
                ],
                
                "avoid_words": ["billig", "enkel", "vanlig", "ordinär"]  # Swedish market values quality and sustainability
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
                
                # Essential Japanese words for natural content
                "essential_words": [
                    "の", "に", "を", "は", "が", "と", "で", "から", "まで", "より",
                    "です", "ます", "である", "ある", "する", "なる", "行く", "来る"
                ],
                
                # Emotional power words for Japanese consumers - EXPANDED for 10/10 quality
                "power_words": [
                    "品質", "信頼性", "機能的", "高品質", "優れた", "性能", "革新",
                    "精密", "効率的", "上質", "特別", "現代的", "先進的", "耐久性",
                    "安心", "便利", "快適", "安全", "丁寧", "美しい", "素晴らしい",
                    "最高", "完璧", "理想的", "実用的", "確実", "卓越", "優秀"
                ],
                
                # Japanese lifestyle and cultural elements - EXPANDED
                "cultural_elements": [
                    "日本品質の証", "きめ細やかな仕上がり", "職人技の品質", 
                    "安心の日本基準", "丁寧な作り込み", "長く愛用できる品質",
                    "毎日の生活をより快適に", "家族みんなで安心してお使いいただけます",
                    "使う人のことを考えた設計", "日本のご家庭に最適"
                ],
                
                # Natural Japanese expressions - EXPANDED  
                "formality_words": [
                    "いただく", "させていただく", "ございます", "でございます",
                    "いらっしゃいます", "お客様", "ご利用", "ご使用", "ご家庭",
                    "安心して", "快適に", "便利に", "長くお使い"
                ],
                
                # Japanese copywriting rules - ENHANCED for comprehensive A+ content
                "enforcement_rules": [
                    "🚨 CRITICAL: ALL content MUST be in Japanese - no English words allowed",
                    "🔥 COMPREHENSIVE A+ CONTENT REQUIREMENTS FOR JAPANESE MARKET:",
                    "✅ Generate ALL 8 A+ content sections with substantial content (minimum 200-300 characters each)",
                    "✅ Each section must include Japanese cultural elements and respectful language",
                    "✅ Use proper Japanese honorific expressions: いただく, ございます, でございます",
                    "✅ Include Japanese quality appreciation: 日本品質, 丁寧な作り, 安心",
                    "✅ Features section: minimum 5 detailed features in Japanese",
                    "✅ Trust section: minimum 4 trust builders with Japanese business language",
                    "✅ Usage section: minimum 3 detailed use cases for Japanese households",
                    "✅ FAQ section: minimum 3 comprehensive Q&A pairs in Japanese",
                    "✅ What's in box: detailed Japanese descriptions of all items",
                    "✅ Testimonials: authentic Japanese customer satisfaction language",
                    "✅ Comparison: advantages explained in Japanese consumer perspective",
                    "✅ Hero section: compelling Japanese marketing language with emotional appeal",
                    "🎯 JAPANESE CONTENT LENGTH REQUIREMENTS:",
                    "- Hero section: 150-200+ characters in Japanese",
                    "- Features section: 300-400+ characters with detailed explanations",
                    "- Trust section: 200-300+ characters with Japanese business credibility",
                    "- Usage section: 250-350+ characters with practical Japanese scenarios",
                    "- FAQ section: 400-500+ characters with comprehensive answers",
                    "- Each section MUST be substantial and informative, not just brief sentences",
                    "🌸 JAPANESE CULTURAL ADAPTATION:",
                    "- Emphasize quality craftsmanship (職人技)",
                    "- Highlight long-term value (長く使える)",
                    "- Include family-oriented benefits (家族で安心)",
                    "- Mention attention to detail (きめ細やか)",
                    "- Use respectful business language throughout",
                    "- Include seasonal considerations where appropriate",
                    "🚫 AVOID: Brief, shallow content - each section must provide real value"
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
        elif marketplace == "se" or language in ["sv", "sv_SE"]:
            market_code = "se"
        elif marketplace == "pl" or language == "pl":
            market_code = "pl"
        elif marketplace in ["co.jp", "jp"] or language == "ja":
            market_code = "ja"
        elif marketplace == "ae" or language == "ar":
            market_code = "ae"
        elif marketplace == "sa" or language in ["ar-sa", "ar_SA"]:
            market_code = "sa"
        elif marketplace == "mx" or language in ["es-mx", "es_MX"]:
            market_code = "mx"
        elif marketplace == "in" or language in ["en-in", "en_IN", "hindi", "hi"]:
            market_code = "in"
        elif marketplace == "br" or language in ["pt-br", "pt_BR", "pt"]:
            market_code = "br"
        elif marketplace == "nl" or language in ["nl", "nl_NL"]:
            market_code = "nl"
        elif marketplace == "se" or language in ["sv", "sv_SE"]:
            market_code = "se"
        elif marketplace == "tr" or language in ["tr", "tr_TR"]:
            market_code = "tr"
        
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
        elif marketplace == "se" or language in ["sv", "sv_SE"]:
            market_code = "se"
        elif marketplace == "pl" or language == "pl":
            market_code = "pl"
        elif marketplace in ["co.jp", "jp"] or language == "ja":
            market_code = "ja"
        elif marketplace == "ae" or language == "ar":
            market_code = "ae"
        elif marketplace == "sa" or language in ["ar-sa", "ar_SA"]:
            market_code = "sa"
        elif marketplace == "mx" or language in ["es-mx", "es_MX"]:
            market_code = "mx"
        elif marketplace == "in" or language in ["en-in", "en_IN", "hindi", "hi"]:
            market_code = "in"
        elif marketplace == "br" or language in ["pt-br", "pt_BR", "pt"]:
            market_code = "br"
        elif marketplace == "nl" or language in ["nl", "nl_NL"]:
            market_code = "nl"
        elif marketplace == "se" or language in ["sv", "sv_SE"]:
            market_code = "se"
        elif marketplace == "tr" or language in ["tr", "tr_TR"]:
            market_code = "tr"
        
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
    "content": "Write comprehensive feature descriptions in {config['language']}",
    "features": ["Feature 1 in {config['language']}", "Feature 2 in {config['language']}", "Feature 3 in {config['language']}", "Feature 4 in {config['language']}", "Feature 5 in {config['language']}"],
    "imageDescription": "ENGLISH: Feature callout grid showing 5-6 key product features with icons and brief descriptions"
  }},
  
  "section3_trust": {{
    "title": "Quality & Trust",  
    "content": "Write comprehensive trust content in {config['language']} emphasizing: {', '.join(cultural_elements)}",
    "trust_builders": ["Trust element 1 in {config['language']}", "Trust element 2 in {config['language']}", "Trust element 3 in {config['language']}", "Trust element 4 in {config['language']}"],
    "imageDescription": "ENGLISH: Trust badges, certifications, and quality indicators relevant to {config['market_name']} market"
  }},
  
  "section4_usage": {{
    "title": "How to Use & Applications",
    "content": "Write detailed usage instructions and applications in {config['language']}",
    "use_cases": ["Use case 1 in {config['language']}", "Use case 2 in {config['language']}", "Use case 3 in {config['language']}"],
    "imageDescription": "ENGLISH: Step-by-step usage guide with visual instructions and real-world applications"
  }},
  
  "section5_comparison": {{
    "title": "Why Choose This Product",
    "content": "Write comparison content highlighting advantages in {config['language']}",
    "advantages": ["Advantage 1 in {config['language']}", "Advantage 2 in {config['language']}", "Advantage 3 in {config['language']}"],
    "imageDescription": "ENGLISH: Comparison chart or before/after showing product benefits vs alternatives"
  }},
  
  "section6_testimonials": {{
    "title": "Customer Satisfaction",
    "content": "Write customer testimonial overview in {config['language']}",
    "testimonials": ["Customer testimonial 1 in {config['language']}", "Customer testimonial 2 in {config['language']}"],
    "imageDescription": "ENGLISH: Customer photos, ratings, and testimonial quotes with star ratings"
  }},
  
  "section7_whats_in_box": {{
    "title": "What's Included",
    "content": "Write complete package contents description in {config['language']}",
    "items": ["Item 1 in {config['language']}", "Item 2 in {config['language']}", "Item 3 in {config['language']}", "Manual/warranty in {config['language']}"],
    "imageDescription": "ENGLISH: Unboxing layout showing all included items with clear labeling"
  }},
  
  "section8_faqs": {{
    "title": "Frequently Asked Questions",
    "content": "Write comprehensive FAQ answers in {config['language']}",
    "faqs": ["Q: Question 1 in {config['language']}? A: Answer 1 in {config['language']}", "Q: Question 2 in {config['language']}? A: Answer 2 in {config['language']}", "Q: Question 3 in {config['language']}? A: Answer 3 in {config['language']}"],
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

🎯 MANDATORY: Generate ALL 8 sections for complete A+ content:
1. section1_hero - REQUIRED
2. section2_features - REQUIRED  
3. section3_usage - REQUIRED
4. section4_quality - REQUIRED
5. section5_guarantee - REQUIRED
6. section6_social_proof - REQUIRED
7. section7_comparison - REQUIRED
8. section8_package - REQUIRED

⚠️ DO NOT skip any sections. Generate complete content for each section to match US/German A+ length.

🇯🇵 SPECIAL REQUIREMENTS FOR JAPANESE MARKET (marketplace: ja/co.jp):
🚨 COMPREHENSIVE JAPANESE A+ CONTENT REQUIREMENTS 🚨
✅ Each section MUST contain 200-400+ characters in Japanese (not just brief sentences)
✅ Hero section: Include emotional appeal with Japanese cultural elements like "日本品質" or "安心"
✅ Features section: MINIMUM 5 detailed features with Japanese quality language
✅ Trust section: Include Japanese business credibility terms like "信頼性" and "丁寧な作り"
✅ Usage section: Provide specific Japanese household scenarios and applications
✅ Comparison section: Highlight advantages using Japanese consumer perspective
✅ FAQ section: MINIMUM 3 comprehensive Q&A pairs in natural Japanese
✅ What's in Box: Detailed descriptions using respectful Japanese language
✅ Testimonials: Authentic Japanese customer satisfaction expressions

🌸 JAPANESE CULTURAL ADAPTATION REQUIREMENTS:
• Use respectful keigo language: ございます, いただく, させていただく
• Emphasize long-term value: 長く使える, 耐久性, 品質
• Include family-oriented benefits: 家族で安心, ご家庭で
• Highlight attention to detail: きめ細やか, 丁寧な
• Use seasonal considerations where appropriate
• Include Japanese quality craftsmanship terminology: 職人技, 日本品質

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