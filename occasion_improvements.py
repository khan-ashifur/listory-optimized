"""
SPECIFIC CODE IMPROVEMENTS FOR 10/10 OCCASION HANDLING

These improvements should be integrated into the _generate_amazon_listing method
in backend/apps/listings/services.py around lines 500-620.

The key changes make occasion the PRIMARY driver when specified,
with adaptive A+ content, enhanced keyword strategies, and tone integration.
"""

# 1. OCCASION-FIRST PROMPT STRUCTURE
# Replace the current occasion handling (lines 509-517) with this enhanced version:

OCCASION_FIRST_PROMPT_STRUCTURE = '''

        # OCCASION-FIRST SYSTEM: Make occasion the PRIMARY organizing principle
        occasion_context = ""
        occasion_keywords = ""
        occasion_emotional_framework = ""
        
        if product.occasion and product.occasion.strip():
            # Define occasion-specific emotional frameworks and keywords
            occasion_data = {
                'christmas': {
                    'emotional_framework': 'joy, warmth, giving, family connection, magical moments, tradition',
                    'primary_keywords': ['christmas gift', 'holiday present', 'festive', 'christmas shopping', 'holiday season', 'winter gift', 'christmas morning', 'holiday joy', 'seasonal favorite', 'gift giving', 'christmas surprise', 'holiday tradition', 'christmas wishlist', 'perfect christmas gift', 'holiday magic'],
                    'gift_context': 'Christmas gift-giving, under the tree, holiday morning surprise, stocking stuffer, Secret Santa, family gathering',
                    'emotional_triggers': ['creates christmas magic', 'brings holiday joy', 'perfect under the tree', 'christmas morning excitement', 'holiday memories', 'festive spirit'],
                    'seasonal_urgency': 'Christmas countdown, last-minute gift, christmas delivery, holiday shopping deadline',
                    'tone_adaptation': {
                        'professional': 'Expertly crafted for the holiday season',
                        'luxury': 'An exquisite Christmas indulgence', 
                        'casual': 'The Christmas gift everyone will love',
                        'playful': 'Christmas magic in every detail',
                        'minimal': 'Simply perfect for Christmas',
                        'bold': 'Dominate Christmas morning'
                    }
                },
                'valentine': {
                    'emotional_framework': 'love, romance, intimacy, passion, devotion, surprise, thoughtfulness',
                    'primary_keywords': ['valentine gift', 'romantic present', 'love gift', "valentine's day", 'romance', 'couples gift', 'date night', 'romantic gesture', 'valentine surprise', 'love language', 'romantic evening', 'valentine special', 'perfect for valentine', 'express your love', 'romantic moment'],
                    'gift_context': "Valentine's Day surprise, romantic dinner, date night, anniversary, expressing love, romantic gesture",
                    'emotional_triggers': ['shows your love', 'romantic surprise', 'perfect valentine gift', 'expresses deep feelings', 'creates romantic moments', 'love language'],
                    'seasonal_urgency': "Valentine's deadline, romantic timing, february 14th delivery, love day preparation",
                    'tone_adaptation': {
                        'professional': 'Professionally crafted for romantic expression',
                        'luxury': 'A luxurious declaration of love',
                        'casual': 'The perfect way to say I love you',
                        'playful': 'Romance with a smile',
                        'minimal': 'Simply romantic',
                        'bold': 'Make a powerful romantic statement'
                    }
                },
                'mother': {
                    'emotional_framework': 'appreciation, gratitude, nurturing, celebration, honor, maternal love, family bonds',
                    'primary_keywords': ['mother day gift', 'mom present', 'mothers day', 'appreciation gift', 'maternal love', 'mom appreciation', 'mother celebration', 'family love', 'grateful for mom', 'motherhood celebration', 'mom deserves', 'mother day surprise', 'perfect for mom', 'honor mom', 'maternal appreciation'],
                    'gift_context': "Mother's Day celebration, showing appreciation, honoring mom, family gathering, maternal recognition",
                    'emotional_triggers': ['shows appreciation', 'honors mom', 'celebrates motherhood', 'perfect for mother day', 'mom deserves this', 'maternal love'],
                    'seasonal_urgency': "Mother's Day delivery, may celebration, mom's special day, appreciation deadline",
                    'tone_adaptation': {
                        'professional': 'Professionally designed to honor mothers',
                        'luxury': 'A luxurious tribute to motherhood',
                        'casual': 'Just what mom deserves',
                        'playful': 'Fun appreciation for amazing moms',
                        'minimal': 'Simply perfect for mom',
                        'bold': 'Powerfully honor the best mom'
                    }
                },
                'father': {
                    'emotional_framework': 'appreciation, respect, strength, guidance, paternal pride, masculine appreciation, family leadership',
                    'primary_keywords': ['father day gift', 'dad present', 'fathers day', 'appreciation gift', 'paternal love', 'dad appreciation', 'father celebration', 'family patriarch', 'grateful for dad', 'fatherhood celebration', 'dad deserves', 'father day surprise', 'perfect for dad', 'honor dad', 'paternal appreciation'],
                    'gift_context': "Father's Day celebration, showing appreciation, honoring dad, family gathering, paternal recognition",
                    'emotional_triggers': ['shows appreciation', 'honors dad', 'celebrates fatherhood', 'perfect for father day', 'dad deserves this', 'paternal respect'],
                    'seasonal_urgency': "Father's Day delivery, june celebration, dad's special day, appreciation deadline",
                    'tone_adaptation': {
                        'professional': 'Professionally crafted to honor fathers',
                        'luxury': 'A premium tribute to fatherhood',
                        'casual': 'Just what dad needs',
                        'playful': 'Fun appreciation for awesome dads',
                        'minimal': 'Simply perfect for dad',
                        'bold': 'Powerfully honor the best dad'
                    }
                },
                'birthday': {
                    'emotional_framework': 'celebration, joy, milestone, personal recognition, special day, age achievement, party spirit',
                    'primary_keywords': ['birthday gift', 'birthday present', 'birthday celebration', 'special birthday', 'birthday surprise', 'milestone birthday', 'birthday joy', 'birthday party', 'age celebration', 'birthday wishes', 'birthday special', 'perfect birthday gift', 'birthday milestone', 'celebration gift', 'birthday memory'],
                    'gift_context': 'Birthday celebration, milestone moment, personal special day, birthday party, age recognition',
                    'emotional_triggers': ['makes birthdays special', 'celebration worthy', 'birthday joy', 'milestone marker', 'special day gift', 'birthday memories'],
                    'seasonal_urgency': 'birthday delivery, special day timing, celebration deadline, birthday surprise timing',
                    'tone_adaptation': {
                        'professional': 'Professionally crafted for birthday celebrations',
                        'luxury': 'A luxurious birthday indulgence',
                        'casual': 'The perfect birthday surprise',
                        'playful': 'Birthday fun in every detail',
                        'minimal': 'Simply perfect for birthdays',
                        'bold': 'Make birthdays unforgettable'
                    }
                }
            }
            
            # Get occasion-specific data or create custom
            occasion_key = None
            for key in occasion_data.keys():
                if key in product.occasion.lower() or product.occasion.lower() in key:
                    occasion_key = key
                    break
            
            if occasion_key:
                occ_data = occasion_data[occasion_key]
                occasion_emotional_framework = occ_data['emotional_framework']
                occasion_keywords = ', '.join(occ_data['primary_keywords'])
                gift_context = occ_data['gift_context']
                emotional_triggers = ', '.join(occ_data['emotional_triggers'])
                seasonal_urgency = occ_data['seasonal_urgency']
                tone_adaptation = occ_data['tone_adaptation'].get(tone_style, f"Expertly crafted for {product.occasion}")
                
                occasion_context = f"""
🎯 OCCASION-FIRST OPTIMIZATION: {product.occasion.upper()}

⚡ CRITICAL: THIS IS AN {product.occasion.upper()} PRODUCT FIRST, EVERYTHING ELSE SECOND!

EMOTIONAL FRAMEWORK: {occasion_emotional_framework}
GIFT CONTEXT: {gift_context}
EMOTIONAL TRIGGERS: {emotional_triggers}
SEASONAL URGENCY: {seasonal_urgency}
TONE ADAPTATION: {tone_adaptation}

OCCASION REQUIREMENTS (NON-NEGOTIABLE):
✅ Title MUST lead with {product.occasion} appeal: "{tone_adaptation} for {product.occasion}" approach
✅ First bullet point MUST be {product.occasion}-focused emotional benefit
✅ Description MUST open with {product.occasion} context and emotional connection
✅ Backend keywords MUST prioritize: {occasion_keywords}
✅ A+ Content MUST use {product.occasion}-specific templates and imagery suggestions
✅ Every section MUST reinforce {product.occasion} emotional resonance
✅ FAQ section MUST include {product.occasion} timing and gift-appropriateness questions

KEYWORD STRATEGY HIERARCHY:
1. Primary: {product.occasion} + emotional triggers (70% weight)
2. Product features (20% weight) 
3. Generic category terms (10% weight)
"""
            else:
                # Custom occasion handling
                occasion_context = f"""
🎯 CUSTOM OCCASION OPTIMIZATION: {product.occasion.upper()}

⚡ CRITICAL: THIS IS A {product.occasion.upper()} PRODUCT FIRST!

CUSTOM OCCASION REQUIREMENTS:
✅ Title MUST emphasize {product.occasion} relevance and timing
✅ Description MUST explain why this is perfect for {product.occasion}
✅ Keywords MUST include: {product.occasion.lower()}, {product.occasion.lower()} gift, perfect for {product.occasion.lower()}, {product.occasion.lower()} celebration, {product.occasion.lower()} present, {product.occasion.lower()} surprise
✅ A+ Content sections MUST tie back to {product.occasion} context
✅ Emotional language MUST match the celebratory/special nature of {product.occasion}
"""
        else:
            occasion_context = "🎯 GENERAL PURPOSE OPTIMIZATION: Create versatile, year-round appeal without seasonal limitations."
'''

# 2. OCCASION-ADAPTIVE A+ CONTENT TEMPLATES
# Replace the generic A+ content templates (lines 617-712) with occasion-aware versions:

OCCASION_ADAPTIVE_APLUS_TEMPLATES = '''
        # Generate A+ content sections that adapt to occasions
        aplus_sections = {}
        
        if product.occasion and product.occasion.strip():
            # Occasion-specific A+ content templates
            if 'christmas' in product.occasion.lower():
                aplus_sections = {
                    "section1_hero": {
                        "title": f"The Perfect Christmas Gift: {product.name}",
                        "content": f"Create magical Christmas moments with this thoughtfully chosen {product_category}. From the excitement of unwrapping to months of enjoyment, this gift delivers genuine Christmas joy that lasts well beyond the holiday season.",
                        "keywords": ["christmas gift", "holiday present", "festive surprise", product.brand_name.lower()],
                        "imageDescription": "Christmas morning scene: product beautifully wrapped under decorated tree, warm fireplace lighting, family gathering atmosphere",
                        "seoOptimization": "Christmas gift primary keyword optimization with brand authority",
                        "cardType": "hero",
                        "cardColor": "festive red and green",
                        "visualTemplate": {
                            "templateType": "holiday-lifestyle",
                            "imageTitle": f"Christmas Magic with {product.brand_name}",
                            "suggestedScene": f"Cozy Christmas morning setting with {product.name} prominently displayed among beautifully wrapped gifts under a decorated tree, warm lighting creates festive atmosphere",
                            "overlayText": "Perfect Christmas Gift • Holiday Joy • Under The Tree",
                            "styleGuide": "Warm Christmas lighting, rich reds and greens, cozy home atmosphere, family-friendly setting that evokes Christmas morning excitement",
                            "layoutStructure": "Product positioned as the star gift, Christmas tree background, warm lighting on product, seasonal decorative elements frame the scene",
                            "colorScheme": "Traditional Christmas colors: deep forest green, warm crimson red, gold accents, cream white background for product contrast",
                            "designElements": ["Christmas tree", "wrapped presents", "fireplace glow", "holiday decorations", "warm lighting", "family setting"]
                        }
                    },
                    "section2_features": {
                        "title": "Holiday-Tested Features",
                        "content": f"Every feature designed with Christmas giving in mind. {product.features if product.features else 'Premium quality construction'} means this gift will be appreciated long after the holidays end, creating lasting memories of your thoughtfulness.",
                        "keywords": ["holiday tested", "christmas quality", "gift features", "lasting value"],
                        "imageDescription": "Product feature callouts with Christmas-themed backgrounds, quality emphasis",
                        "seoOptimization": "Feature-based Christmas gift keywords",
                        "cardType": "features",
                        "cardColor": "holiday gold",
                        "visualTemplate": {
                            "templateType": "christmas-infographic",
                            "imageTitle": "Holiday-Perfect Features",
                            "suggestedScene": f"{product.name} with elegant Christmas-themed feature callouts, premium presentation against festive background",
                            "overlayText": "Built for Christmas Joy • Quality That Lasts • Gift-Worthy Features",
                            "styleGuide": "Premium product photography with Christmas elegance, clean callout design, sophisticated holiday aesthetic",
                            "layoutStructure": "Product centered with 4-5 feature callouts arranged in elegant Christmas ornament pattern, premium gift presentation",
                            "colorScheme": "Sophisticated Christmas palette: deep evergreen, warm gold, ivory white, rich burgundy accents for premium feel",
                            "designElements": ["feature callouts", "Christmas ornament styling", "premium quality badges", "holiday elegance", "gift presentation"]
                        }
                    }
                }
            elif 'valentine' in product.occasion.lower():
                aplus_sections = {
                    "section1_hero": {
                        "title": f"Express Your Love: {product.name}",
                        "content": f"Some gifts say 'I love you' better than words ever could. This {product_category} becomes a daily reminder of your love and thoughtfulness, creating romantic moments that last far beyond Valentine's Day.",
                        "keywords": ["valentine gift", "romantic present", "love expression", product.brand_name.lower()],
                        "imageDescription": "Romantic Valentine's scene: product elegantly presented with roses and soft candlelight, intimate dinner setting",
                        "seoOptimization": "Valentine's Day romantic gift keywords with emotional appeal",
                        "cardType": "hero", 
                        "cardColor": "romantic red and pink",
                        "visualTemplate": {
                            "templateType": "romantic-lifestyle",
                            "imageTitle": f"A Love Letter in Every Detail",
                            "suggestedScene": f"Intimate romantic setting with {product.name} beautifully displayed alongside red roses, soft candlelight, elegant dinner table for two",
                            "overlayText": "Perfect Valentine's Gift • Express Your Love • Romantic Surprise",
                            "styleGuide": "Soft romantic lighting, elegant intimate atmosphere, luxurious romantic elements, warm and inviting mood",
                            "layoutStructure": "Product as romantic centerpiece, roses and candles frame the scene, intimate dining setting background",
                            "colorScheme": "Romantic Valentine's palette: deep passionate red, soft blush pink, warm gold highlights, cream background for elegance",
                            "designElements": ["red roses", "candlelight", "elegant table setting", "romantic atmosphere", "intimate lighting", "love symbols"]
                        }
                    }
                }
            elif 'mother' in product.occasion.lower():
                aplus_sections = {
                    "section1_hero": {
                        "title": f"Honor Mom with {product.name}",
                        "content": f"Mothers deserve the very best, and this {product_category} delivers exactly that. Show your appreciation with a gift that acknowledges all she does and gives her something wonderful just for herself.",
                        "keywords": ["mother day gift", "mom appreciation", "maternal love", product.brand_name.lower()],
                        "imageDescription": "Mother's Day celebration: product presented in elegant family setting, flowers and appreciation theme",
                        "seoOptimization": "Mother's Day gift keywords with appreciation focus",
                        "cardType": "hero",
                        "cardColor": "soft maternal pink and lavender", 
                        "visualTemplate": {
                            "templateType": "family-appreciation",
                            "imageTitle": f"Because Mom Deserves the Best",
                            "suggestedScene": f"Warm family kitchen or living room with {product.name} beautifully presented, spring flowers, family photos, nurturing home atmosphere",
                            "overlayText": "Perfect for Mom • Mother's Day Gift • She Deserves This",
                            "styleGuide": "Warm family home lighting, nurturing maternal atmosphere, appreciative and loving mood, spring garden elements",
                            "layoutStructure": "Product displayed in loving family context, spring flowers accent, family memories in background",
                            "colorScheme": "Maternal appreciation colors: soft lavender, warm rose, gentle cream, spring green accents for nurturing feel",
                            "designElements": ["spring flowers", "family photos", "home atmosphere", "maternal warmth", "appreciation theme", "nurturing setting"]
                        }
                    }
                }
        else:
            # Regular A+ content sections (non-occasion)
            aplus_sections = {
                "section1_hero": {
                    "title": f"Discover {product.name}",
                    "content": f"Experience the difference that thoughtful design makes. This {product_category} combines innovative features with reliable performance to enhance your daily routine in meaningful ways.",
                    "keywords": [product.brand_name.lower(), product_category.lower(), "innovative design", "reliable performance"],
                    "imageDescription": "Clean lifestyle product showcase in modern setting, professional use context",
                    "seoOptimization": "Brand authority and product category leadership",
                    "cardType": "hero",
                    "cardColor": "professional blue",
                    "visualTemplate": {
                        "templateType": "modern-lifestyle",
                        "imageTitle": f"Experience {product.brand_name} Excellence",
                        "suggestedScene": f"Modern, clean environment showcasing {product.name} in professional daily use context, natural lighting, contemporary setting",
                        "overlayText": "Innovative Design • Reliable Performance • Daily Excellence",
                        "styleGuide": "Clean modern aesthetic, professional lighting, contemporary style, focused on product excellence",
                        "layoutStructure": "Product prominently featured in clean modern setting, minimalist background, professional presentation",
                        "colorScheme": "Modern professional palette: clean white, sophisticated gray, brand color accents, contemporary feel",
                        "designElements": ["clean lines", "modern setting", "professional context", "brand excellence", "quality focus", "contemporary style"]
                    }
                }
            }
'''

# 3. ENHANCED KEYWORD STRATEGY FOR OCCASIONS
# Replace the keyword generation logic with occasion-prioritized approach:

OCCASION_KEYWORD_STRATEGY = '''
        # Enhanced keyword generation with occasion priority
        def generate_occasion_optimized_keywords():
            base_keywords = []
            
            # Start with product fundamentals
            if product.name:
                base_keywords.extend([product.name.lower(), product.brand_name.lower()])
            
            # Add features and categories
            if product.features:
                features = [f.strip().lower() for f in product.features.split(',') if f.strip()]
                base_keywords.extend(features[:5])
                
            if product.categories:
                categories = [c.strip().lower() for c in product.categories.split(',') if c.strip()]
                base_keywords.extend(categories[:3])
            
            # Occasion-first keyword expansion
            if product.occasion and product.occasion.strip():
                occasion = product.occasion.lower()
                
                # High-priority occasion keywords (70% of keyword strategy)
                occasion_primary = [
                    f"{occasion} gift",
                    f"{occasion} present", 
                    f"perfect {occasion} gift",
                    f"{occasion} surprise",
                    f"best {occasion} gift",
                    f"{occasion} shopping",
                    f"{occasion} celebration",
                    f"ideal {occasion} present",
                    f"{occasion} special",
                    f"{occasion} favorite"
                ]
                
                # Combine with product
                product_occasion_combo = [
                    f"{product.name.lower()} for {occasion}",
                    f"{occasion} {product_category.lower()}",
                    f"{product.brand_name.lower()} {occasion} gift",
                    f"{occasion} {product.brand_name.lower()}",
                    f"best {product_category.lower()} for {occasion}",
                ]
                
                # Long-tail occasion phrases
                occasion_longtail = [
                    f"what to get for {occasion}",
                    f"best {occasion} gifts for {product.target_audience[:20] if hasattr(product, 'target_audience') and product.target_audience else 'everyone'}",
                    f"{occasion} gift ideas",
                    f"perfect {occasion} present for",
                    f"last minute {occasion} gifts",
                    f"{occasion} gift delivery",
                    f"unique {occasion} gifts",
                    f"thoughtful {occasion} presents",
                    f"{occasion} gift under {int(float(product.price) + 50) if product.price else '100'}",
                    f"memorable {occasion} gifts"
                ]
                
                # Problem-solving occasion keywords
                occasion_problems = [
                    f"running out of {occasion} gift ideas",
                    f"need {occasion} gift fast",
                    f"what do you get someone for {occasion}",
                    f"best {occasion} gifts that actually get used",
                    f"meaningful {occasion} presents",
                    f"{occasion} gifts that show you care"
                ]
                
                return {
                    "primary": base_keywords + occasion_primary[:10],
                    "longTail": occasion_longtail + product_occasion_combo,
                    "problemSolving": occasion_problems,
                    "rufusConversational": [
                        f"good {product.name.lower()} for {occasion}",
                        f"works as {occasion} gift", 
                        f"perfect for {occasion}",
                        f"better than other {occasion} gifts",
                        f"ideal for {occasion} celebration",
                        f"worth it for {occasion}",
                        f"appropriate {occasion} gift",
                        f"recommended for {occasion}",
                        f"suitable {occasion} present",
                        f"fits {occasion} budget"
                    ],
                    "semantic": [
                        occasion,
                        f"{occasion}time",
                        "celebration",
                        "gift giving",
                        "present",
                        "surprise",
                        "special occasion",
                        "holiday",
                        "festive",
                        "seasonal"
                    ]
                }
            else:
                # Regular keyword strategy for non-occasion products
                product_longtail = [
                    f"best {product_category.lower()}",
                    f"{product.brand_name.lower()} {product_category.lower()}",
                    f"top rated {product_category.lower()}",
                    f"professional {product_category.lower()}",
                    f"high quality {product_category.lower()}"
                ]
                
                return {
                    "primary": base_keywords + [product_category.lower(), "professional", "high quality", "reliable", "durable"],
                    "longTail": product_longtail,
                    "problemSolving": [
                        f"need reliable {product_category.lower()}",
                        f"looking for quality {product_category.lower()}",
                        f"best value {product_category.lower()}"
                    ],
                    "rufusConversational": [
                        f"good {product_category.lower()}",
                        f"works well",
                        f"better than competitors",
                        f"worth the price",
                        f"recommended {product_category.lower()}"
                    ],
                    "semantic": [
                        product_category.lower(),
                        "professional grade",
                        "premium quality",
                        "reliable performance"
                    ]
                }
'''

# 4. TITLE OPTIMIZATION WITH OCCASION-FIRST APPROACH
# Insert this logic before the title generation section:

TITLE_OPTIMIZATION_LOGIC = '''
        # Occasion-first title optimization
        def generate_optimized_title():
            brand = product.brand_name
            product_name = product.name
            
            if product.occasion and product.occasion.strip():
                occasion = product.occasion
                
                # Occasion-first title templates based on tone
                if tone_style == 'professional':
                    title_template = f"Professional {occasion} Gift: {brand} {product_name} - Premium Quality for Special Celebrations"
                elif tone_style == 'luxury':
                    title_template = f"Luxurious {occasion} Present: {brand} {product_name} - Exquisite Gift for Discerning Recipients"  
                elif tone_style == 'casual':
                    title_template = f"Perfect {occasion} Gift: {brand} {product_name} - Everyone Will Love This Surprise"
                elif tone_style == 'playful':
                    title_template = f"Amazing {occasion} Surprise: {brand} {product_name} - Gift That Brings Smiles"
                elif tone_style == 'minimal':
                    title_template = f"{brand} {product_name} - Perfect {occasion} Gift"
                elif tone_style == 'bold':
                    title_template = f"Ultimate {occasion} Gift: {brand} {product_name} - Make Their Day Unforgettable"
                else:
                    title_template = f"{brand} {product_name} - Perfect {occasion} Gift"
                    
                # Ensure title is under 200 characters
                if len(title_template) > 180:
                    title_template = f"{brand} {product_name} - Perfect {occasion} Gift"
                    
                return title_template
            else:
                # Regular title for non-occasion products
                primary_benefit = features_list[0] if features_list else "Premium Quality"
                title_template = f"{brand} {product_name} - {primary_benefit} {product_category}"
                
                return title_template
'''

print("CODE IMPROVEMENTS READY FOR INTEGRATION")
print("These improvements will make occasion the PRIMARY driver when specified.")
print("Key changes:")
print("1. Occasion-first prompt structure with emotional frameworks")
print("2. Adaptive A+ content templates for each major occasion") 
print("3. Enhanced keyword strategy prioritizing occasion terms")
print("4. Title optimization with occasion-first approach")
print("5. Tone adaptation that works with occasions")