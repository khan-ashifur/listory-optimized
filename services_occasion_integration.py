"""
DIRECT INTEGRATION CODE FOR SERVICES.PY
Replace lines 505-517 and enhance the prompt generation for 10/10 occasion handling
"""

def get_enhanced_occasion_prompt_section(product, tone_style, product_category):
    """
    Generate the enhanced occasion-first prompt section
    This replaces the current basic occasion handling
    """
    
    if not product.occasion or not product.occasion.strip():
        return "🎯 GENERAL PURPOSE OPTIMIZATION: Create versatile, year-round appeal without seasonal limitations."
    
    # Define comprehensive occasion data
    occasion_data = {
        'christmas': {
            'emotional_framework': 'joy, warmth, giving, family connection, magical moments, tradition, celebration, excitement, festive spirit, holiday magic',
            'primary_keywords': ['christmas gift', 'holiday present', 'festive', 'christmas shopping', 'holiday season', 'winter gift', 'christmas morning', 'holiday joy', 'seasonal favorite', 'gift giving', 'christmas surprise', 'holiday tradition', 'christmas wishlist', 'perfect christmas gift', 'holiday magic', 'christmas tree', 'santa gift', 'stocking stuffer', 'holiday celebration', 'christmas special'],
            'gift_context': 'Christmas gift-giving, under the tree, holiday morning surprise, stocking stuffer, Secret Santa, family gathering, christmas wish fulfillment, holiday shopping',
            'emotional_triggers': ['creates christmas magic', 'brings holiday joy', 'perfect under the tree', 'christmas morning excitement', 'holiday memories that last', 'festive spirit', 'christmas wish come true', 'holiday tradition maker'],
            'seasonal_urgency': 'Christmas countdown, last-minute christmas gift, christmas delivery deadline, holiday shopping urgency, christmas morning ready',
            'tone_adaptations': {
                'professional': 'Professionally crafted for the Christmas season - trusted quality for holiday gifting',
                'luxury': 'An exquisite Christmas indulgence that transforms holiday celebrations into luxury experiences',
                'casual': 'The Christmas gift everyone will love - perfect for making holiday memories together',
                'playful': 'Christmas magic in every detail - bringing smiles to faces on Christmas morning',
                'minimal': 'Simply perfect for Christmas - elegant holiday gifting made effortless',
                'bold': 'Dominate Christmas morning with this unforgettable holiday surprise'
            },
            'a_plus_focus': 'Christmas lifestyle imagery, holiday family moments, gift-giving scenarios, festive home settings, christmas morning scenes',
            'title_pattern': 'Perfect Christmas Gift: [BRAND] [PRODUCT] - Holiday Joy for Everyone'
        },
        'valentine': {
            'emotional_framework': 'love, romance, intimacy, passion, devotion, surprise, thoughtfulness, connection, adoration, romantic gesture, heart-warming',
            'primary_keywords': ['valentine gift', 'romantic present', 'love gift', "valentine's day", 'romance', 'couples gift', 'date night', 'romantic gesture', 'valentine surprise', 'love language', 'romantic evening', 'valentine special', 'perfect valentine gift', 'express your love', 'romantic moment', 'love token', 'valentine romance', 'heart gift', 'romantic surprise', 'love expression'],
            'gift_context': "Valentine's Day surprise, romantic dinner, date night enhancement, anniversary celebration, expressing deep love, romantic gesture, couple bonding, intimate moments",
            'emotional_triggers': ['shows your love perfectly', 'romantic surprise that touches the heart', 'perfect valentine expression', 'demonstrates deep feelings', 'creates romantic moments', 'speaks your love language', 'unforgettable romantic gesture', 'love made tangible'],
            'seasonal_urgency': "Valentine's Day deadline approaching, February 14th delivery, romantic timing crucial, love day preparation, valentine surprise timing",
            'tone_adaptations': {
                'professional': 'Professionally designed for romantic expression - sophisticated love language',
                'luxury': 'A luxurious declaration of love that transforms ordinary moments into romantic memories',
                'casual': 'The perfect way to say I love you - romance made simple and heartfelt',
                'playful': 'Romance with a smile - love that brings joy and laughter together',
                'minimal': 'Simply romantic - elegant love expression without complications',
                'bold': 'Make a powerful romantic statement that will be remembered forever'
            },
            'a_plus_focus': 'Romantic dinner settings, intimate moments, couple photography, elegant romantic styling, valentine date scenarios',
            'title_pattern': 'Perfect Valentine Gift: [BRAND] [PRODUCT] - Express Your Love Beautifully'
        },
        'mother': {
            'emotional_framework': 'appreciation, gratitude, nurturing celebration, maternal honor, family love, thankfulness, recognition, caring, devotion, respect for motherhood',
            'primary_keywords': ['mother day gift', 'mom present', 'mothers day', 'appreciation gift', 'maternal love', 'mom appreciation', 'mother celebration', 'family love', 'grateful for mom', 'motherhood celebration', 'mom deserves best', 'mother day surprise', 'perfect for mom', 'honor mom', 'maternal appreciation', 'mom love', 'mother tribute', 'family matriarch', 'caring mom gift', 'nurturing mother'],
            'gift_context': "Mother's Day celebration, showing deep appreciation, honoring mom's sacrifices, family gathering, maternal recognition, thanking mom for everything, celebrating motherhood",
            'emotional_triggers': ['shows genuine appreciation', 'honors incredible mom', 'celebrates motherhood beautifully', 'perfect mother day tribute', 'mom truly deserves this', 'maternal love acknowledged', 'family gratitude expressed', 'motherhood celebrated properly'],
            'seasonal_urgency': "Mother's Day delivery essential, May celebration timing, mom's special day approaching, appreciation deadline, motherhood honor day",
            'tone_adaptations': {
                'professional': 'Professionally designed to honor mothers with the respect and quality they deserve',
                'luxury': 'A luxurious tribute to motherhood - celebrating mom with premium elegance she merits',
                'casual': 'Just what mom deserves - appreciation made simple but meaningful',
                'playful': 'Fun appreciation for amazing moms who make life brighter every day',
                'minimal': 'Simply perfect for mom - elegant appreciation without fuss',
                'bold': 'Powerfully honor the best mom with a gift as strong as her love'
            },
            'a_plus_focus': 'Family home settings, maternal nurturing scenes, mother-child moments, appreciation ceremonies, spring flowers and family warmth',
            'title_pattern': 'Perfect Mother\'s Day Gift: [BRAND] [PRODUCT] - Honor Mom with Quality She Deserves'
        },
        'father': {
            'emotional_framework': 'appreciation, respect, strength recognition, paternal honor, masculine appreciation, family leadership acknowledgment, gratitude, admiration',
            'primary_keywords': ['father day gift', 'dad present', 'fathers day', 'paternal appreciation', 'dad gift', 'father appreciation', 'father celebration', 'family patriarch', 'grateful for dad', 'fatherhood celebration', 'dad deserves best', 'father day surprise', 'perfect for dad', 'honor dad', 'paternal respect', 'dad love', 'father tribute', 'family leader', 'caring dad gift', 'strong father'],
            'gift_context': "Father's Day celebration, showing appreciation for dad, honoring paternal guidance, family recognition, celebrating fatherhood, acknowledging dad's strength and support",
            'emotional_triggers': ['shows genuine appreciation for dad', 'honors incredible father', 'celebrates fatherhood strength', 'perfect father day tribute', 'dad truly deserves this recognition', 'paternal love acknowledged', 'family gratitude for dad', 'fatherhood celebrated with respect'],
            'seasonal_urgency': "Father's Day delivery crucial, June celebration timing, dad's special day approaching, appreciation deadline, fatherhood honor day",
            'tone_adaptations': {
                'professional': 'Professionally crafted to honor fathers with the respect and recognition they deserve',
                'luxury': 'A premium tribute to fatherhood - celebrating dad with the quality that matches his character',
                'casual': 'Just what dad needs - practical appreciation he will actually use and enjoy',
                'playful': 'Fun appreciation for awesome dads who make family life an adventure',
                'minimal': 'Simply perfect for dad - straightforward quality he will respect',
                'bold': 'Powerfully honor the best dad with strength that matches his dedication'
            },
            'a_plus_focus': 'Father-child bonding moments, family leadership scenes, dad hobby contexts, paternal strength imagery, family gathering celebrations',
            'title_pattern': 'Perfect Father\'s Day Gift: [BRAND] [PRODUCT] - Quality Dad Deserves and Will Use'
        },
        'birthday': {
            'emotional_framework': 'celebration, joy, milestone recognition, personal honor, life celebration, happiness, festivity, achievement recognition, special day magic',
            'primary_keywords': ['birthday gift', 'birthday present', 'birthday celebration', 'special birthday', 'birthday surprise', 'milestone birthday', 'birthday joy', 'birthday party', 'age celebration', 'birthday wishes', 'birthday special', 'perfect birthday gift', 'birthday milestone', 'celebration gift', 'birthday memory', 'personal celebration', 'birthday happiness', 'special day gift', 'birthday festivity', 'life celebration'],
            'gift_context': 'Birthday celebration moments, milestone achievements, personal special day recognition, birthday party enjoyment, age celebration, life milestone marking',
            'emotional_triggers': ['makes birthdays truly special', 'celebration-worthy surprise', 'birthday joy amplified', 'milestone perfectly marked', 'special day made memorable', 'birthday magic created', 'personal celebration enhanced', 'life moment honored'],
            'seasonal_urgency': 'birthday delivery timing crucial, special day approaching, celebration preparation needed, birthday surprise timing, milestone moment ready',
            'tone_adaptations': {
                'professional': 'Professionally crafted for birthday celebrations - quality that honors life milestones appropriately',
                'luxury': 'A luxurious birthday indulgence that transforms special days into extraordinary celebrations',
                'casual': 'The perfect birthday surprise that brings genuine smiles and lasting happiness',
                'playful': 'Birthday fun in every detail - celebration joy that makes special days unforgettable',
                'minimal': 'Simply perfect for birthdays - elegant celebration without complicated fuss',
                'bold': 'Make birthdays absolutely unforgettable with celebration power that creates lasting memories'
            },
            'a_plus_focus': 'Birthday party scenes, celebration moments, milestone imagery, festive atmospheres, personal joy and happiness contexts',
            'title_pattern': 'Perfect Birthday Gift: [BRAND] [PRODUCT] - Make Their Special Day Unforgettable'
        }
    }
    
    # Find matching occasion data
    occasion_key = None
    occasion_lower = product.occasion.lower()
    
    for key in occasion_data.keys():
        if key in occasion_lower or occasion_lower in key:
            occasion_key = key
            break
    
    if occasion_key:
        occ_data = occasion_data[occasion_key]
        tone_adaptation = occ_data['tone_adaptations'].get(tone_style, f"Expertly crafted for {product.occasion}")
        
        return f"""
🎯 OCCASION-FIRST OPTIMIZATION: {product.occasion.upper()} IS THE PRIMARY FOCUS

⚡ CRITICAL DIRECTIVE: THIS IS A {product.occasion.upper()} PRODUCT FIRST, {product_category.upper()} SECOND!

EMOTIONAL FRAMEWORK: {occ_data['emotional_framework']}
GIFT CONTEXT: {occ_data['gift_context']}
EMOTIONAL TRIGGERS: {', '.join(occ_data['emotional_triggers'])}
SEASONAL URGENCY: {occ_data['seasonal_urgency']}
TONE INTEGRATION: {tone_adaptation}

NON-NEGOTIABLE {product.occasion.upper()} REQUIREMENTS:
✅ TITLE: Must lead with "{product.occasion}" emotional appeal using pattern: {occ_data['title_pattern']}
✅ OPENING BULLET: Must be {product.occasion}-focused emotional benefit (not product feature)
✅ DESCRIPTION: Must open with {product.occasion} context before product details
✅ BACKEND KEYWORDS: Must prioritize {product.occasion} terms: {', '.join(occ_data['primary_keywords'][:15])}
✅ A+ CONTENT: Must use {product.occasion}-specific visual themes: {occ_data['a_plus_focus']}
✅ FAQ SECTION: Must include {product.occasion} timing, appropriateness, and gift-value questions
✅ ALL SECTIONS: Must reinforce {product.occasion} emotional resonance throughout

KEYWORD HIERARCHY FOR {product.occasion.upper()}:
Priority 1 (70%): {product.occasion} + emotional benefits
Priority 2 (20%): Product features that enhance {product.occasion} value  
Priority 3 (10%): Generic product category terms

VISUAL TEMPLATE REQUIREMENTS:
- All A+ content images must incorporate {product.occasion} lifestyle contexts
- Color schemes must reflect {product.occasion} emotional palette
- Scene suggestions must place product in {product.occasion} scenarios
- Layout structures must emphasize {product.occasion} gift-giving contexts

EMOTIONAL LANGUAGE MANDATE:
Every sentence must contribute to {product.occasion} emotional experience. Replace functional language with emotional benefits that connect to {product.occasion} feelings and occasions.
"""
    else:
        # Custom occasion handling for non-standard occasions
        return f"""
🎯 CUSTOM OCCASION OPTIMIZATION: {product.occasion.upper()} IS THE PRIMARY FOCUS

⚡ CRITICAL: THIS IS A {product.occasion.upper()} PRODUCT FIRST!

CUSTOM OCCASION REQUIREMENTS:
✅ TITLE: Must emphasize "{product.occasion}" relevance and perfect timing for this special occasion
✅ DESCRIPTION: Must explain why this is specifically perfect for {product.occasion} celebrations
✅ KEYWORDS: Must prioritize: {product.occasion.lower()}, {product.occasion.lower()} gift, perfect for {product.occasion.lower()}, {product.occasion.lower()} celebration, {product.occasion.lower()} present, {product.occasion.lower()} surprise, ideal {product.occasion.lower()} choice
✅ A+ CONTENT: All sections must tie back to {product.occasion} celebration context and timing
✅ EMOTIONAL LANGUAGE: Must match the celebratory and special nature of {product.occasion}
✅ GIFT VALUE: Must emphasize why this makes an appropriate and thoughtful {product.occasion} gift

KEYWORD FOCUS: {product.occasion} celebration, gift-giving, special occasion, perfect timing, thoughtful present
"""


def get_enhanced_aplus_content_structure(product, product_category):
    """
    Generate occasion-adaptive A+ content structure
    This replaces the generic A+ content templates
    """
    
    if not product.occasion or not product.occasion.strip():
        # Return standard professional A+ content for non-occasion products
        return '''
    "section1_hero": {
      "title": "Experience Professional Excellence",
      "content": "Discover the difference that thoughtful engineering makes. This premium ''' + product_category + ''' combines innovative features with reliable performance to enhance your daily routine in meaningful ways.",
      "keywords": ["''' + product.brand_name.lower() + '''", "''' + product_category.lower() + '''", "professional grade", "premium quality"],
      "imageDescription": "Clean lifestyle product showcase in modern professional setting, natural lighting",
      "seoOptimization": "Brand authority and product category leadership focus",
      "cardType": "hero",
      "cardColor": "professional blue",
      "visualTemplate": {
        "templateType": "modern-lifestyle",
        "imageTitle": "Experience ''' + product.brand_name + ''' Professional Excellence",
        "suggestedScene": "Modern, clean environment showcasing ''' + product.name + ''' in professional daily use context with natural lighting and contemporary setting",
        "overlayText": "Professional Grade • Premium Quality • Reliable Performance",
        "styleGuide": "Clean modern aesthetic with professional lighting and contemporary style focused on product excellence",
        "layoutStructure": "Product prominently featured in clean modern setting with minimalist background and professional presentation",
        "colorScheme": "Modern professional palette: clean white, sophisticated gray, brand color accents with contemporary feel",
        "designElements": ["clean lines", "modern setting", "professional context", "brand excellence", "quality focus", "contemporary style"]
      }
    }'''
    
    # Occasion-specific A+ content generation
    occasion_lower = product.occasion.lower()
    
    if 'christmas' in occasion_lower:
        return '''
    "section1_hero": {
      "title": "The Perfect Christmas Gift: ''' + product.name + '''",
      "content": "Create magical Christmas moments with this thoughtfully chosen ''' + product_category + '''. From the excitement of unwrapping to months of enjoyment afterward, this gift delivers genuine Christmas joy that extends well beyond the holiday season. Every detail designed with gift-giving in mind.",
      "keywords": ["christmas gift", "holiday present", "festive surprise", "''' + product.brand_name.lower() + '''", "christmas magic"],
      "imageDescription": "Warm Christmas morning scene: product beautifully wrapped under decorated tree with fireplace lighting and family gathering atmosphere",
      "seoOptimization": "Christmas gift primary keyword optimization combined with brand authority",
      "cardType": "hero",
      "cardColor": "festive red and green",
      "visualTemplate": {
        "templateType": "christmas-lifestyle",
        "imageTitle": "Christmas Magic with ''' + product.brand_name + '''",
        "suggestedScene": "Cozy Christmas morning setting with ''' + product.name + ''' prominently displayed among beautifully wrapped gifts under decorated tree, warm fireplace lighting creates festive family atmosphere",
        "overlayText": "Perfect Christmas Gift • Holiday Joy • Under The Tree",
        "styleGuide": "Warm Christmas lighting with rich reds and greens, cozy home atmosphere that evokes Christmas morning excitement and family gathering warmth",
        "layoutStructure": "Product positioned as the featured Christmas gift, decorated tree background, warm lighting highlights product, seasonal decorative elements frame the scene",
        "colorScheme": "Traditional Christmas palette: deep forest green, warm crimson red, gold accents, cream white background for product contrast",
        "designElements": ["Christmas tree", "wrapped presents", "fireplace glow", "holiday decorations", "warm lighting", "family gathering setting"]
      }
    },
    "section2_features": {
      "title": "Holiday-Perfect Features for Gift Giving",
      "content": "Every feature carefully designed with Christmas gift recipients in mind. ''' + (product.features if product.features else 'Premium quality construction and thoughtful design') + ''' ensures this gift will be treasured long after the holidays end, creating lasting memories of your thoughtfulness and care.",
      "keywords": ["christmas quality", "holiday features", "gift-worthy", "lasting value", "christmas tested"],
      "imageDescription": "Elegant product feature showcase with Christmas-themed presentation, premium gift-worthy quality emphasis",
      "seoOptimization": "Christmas gift feature keywords combined with quality emphasis",
      "cardType": "features", 
      "cardColor": "holiday gold",
      "visualTemplate": {
        "templateType": "christmas-infographic",
        "imageTitle": "Holiday-Perfect Gift Features",
        "suggestedScene": "''' + product.name + ''' with elegant Christmas-themed feature callouts in premium presentation against sophisticated holiday background",
        "overlayText": "Gift-Worthy Quality • Holiday Tested • Christmas Perfect",
        "styleGuide": "Premium product photography with Christmas elegance, clean feature callout design, sophisticated holiday aesthetic that emphasizes gift value",
        "layoutStructure": "Product centered with 4-5 feature callouts arranged in elegant pattern, premium Christmas gift presentation with holiday styling",
        "colorScheme": "Sophisticated Christmas palette: deep evergreen, warm gold, ivory white, rich burgundy accents for premium gift feel",
        "designElements": ["feature callouts", "Christmas elegance", "premium gift presentation", "holiday styling", "gift-worthy badges"]
      }
    }'''
    
    elif 'valentine' in occasion_lower:
        return '''
    "section1_hero": {
      "title": "Express Your Love: ''' + product.name + '''",
      "content": "Some gifts express 'I love you' better than words ever could. This ''' + product_category + ''' becomes a daily reminder of your love and thoughtfulness, creating romantic moments that last far beyond Valentine's Day. Perfect for showing someone how much they mean to you.",
      "keywords": ["valentine gift", "romantic present", "love expression", "''' + product.brand_name.lower() + '''", "valentine romance"],
      "imageDescription": "Romantic Valentine scene: product elegantly presented with red roses and soft candlelight in intimate dinner setting",
      "seoOptimization": "Valentine's Day romantic gift keywords with emotional love appeal",
      "cardType": "hero",
      "cardColor": "romantic red and pink", 
      "visualTemplate": {
        "templateType": "romantic-lifestyle",
        "imageTitle": "A Love Letter in Every Detail",
        "suggestedScene": "Intimate romantic setting with ''' + product.name + ''' beautifully displayed alongside dozen red roses, soft candlelight, elegant dinner table set for romantic evening for two",
        "overlayText": "Perfect Valentine Gift • Express Your Love • Romantic Surprise",
        "styleGuide": "Soft romantic lighting with elegant intimate atmosphere, luxurious romantic elements create warm and inviting mood perfect for Valentine's Day",
        "layoutStructure": "Product as romantic centerpiece with roses and candles framing the scene, intimate dining setting provides romantic background context",
        "colorScheme": "Romantic Valentine palette: deep passionate red, soft blush pink, warm gold highlights, cream background for elegant romantic feel",
        "designElements": ["red roses", "candlelight", "elegant table setting", "romantic atmosphere", "intimate lighting", "love symbols"]
      }
    }'''
    
    elif 'mother' in occasion_lower:
        return '''
    "section1_hero": {
      "title": "Honor Mom with ''' + product.name + '''",
      "content": "Mothers deserve the very best, and this ''' + product_category + ''' delivers exactly that level of quality and thoughtfulness. Show your deep appreciation with a gift that acknowledges all she does and gives her something wonderful that's just for herself. Because mom deserves to be celebrated.",
      "keywords": ["mother day gift", "mom appreciation", "maternal love", "''' + product.brand_name.lower() + '''", "honor mom"],
      "imageDescription": "Warm Mother's Day celebration: product presented in elegant family home setting with spring flowers and appreciation theme",
      "seoOptimization": "Mother's Day gift keywords with appreciation and maternal love focus",
      "cardType": "hero",
      "cardColor": "soft maternal pink and lavender",
      "visualTemplate": {
        "templateType": "family-appreciation",
        "imageTitle": "Because Mom Deserves the Very Best",
        "suggestedScene": "Warm family kitchen or living room with ''' + product.name + ''' beautifully presented, fresh spring flowers, family photos, nurturing home atmosphere that celebrates motherhood",
        "overlayText": "Perfect for Mom • Mother's Day Gift • She Deserves This",
        "styleGuide": "Warm family home lighting with nurturing maternal atmosphere, appreciative and loving mood enhanced by spring garden elements and family warmth",
        "layoutStructure": "Product displayed in loving family context with spring flowers as accent, family memories visible in background to emphasize maternal appreciation",
        "colorScheme": "Maternal appreciation colors: soft lavender, warm rose, gentle cream, spring green accents create nurturing and appreciative feel",
        "designElements": ["spring flowers", "family photos", "home atmosphere", "maternal warmth", "appreciation theme", "nurturing family setting"]
      }
    }'''
    
    else:
        # Custom occasion A+ content
        return '''
    "section1_hero": {
      "title": "Perfect for ''' + product.occasion + ''': ''' + product.name + '''",
      "content": "Celebrate ''' + product.occasion + ''' with a gift that shows true thoughtfulness. This ''' + product_category + ''' is specifically chosen for ''' + product.occasion + ''' celebrations, ensuring your gift will be remembered and appreciated long after the special day ends.",
      "keywords": ["''' + product.occasion.lower() + ''' gift", "''' + product.occasion.lower() + ''' present", "celebration gift", "''' + product.brand_name.lower() + '''"],
      "imageDescription": "''' + product.occasion + ''' celebration scene: product elegantly presented in appropriate ''' + product.occasion.lower() + ''' context with celebratory atmosphere",
      "seoOptimization": "''' + product.occasion + ''' gift keywords with celebration and special occasion focus",
      "cardType": "hero", 
      "cardColor": "celebration theme appropriate",
      "visualTemplate": {
        "templateType": "celebration-lifestyle",
        "imageTitle": "Perfect ''' + product.occasion + ''' Gift Choice",
        "suggestedScene": "''' + product.occasion + ''' celebration setting with ''' + product.name + ''' prominently featured in appropriate celebratory context and atmosphere",
        "overlayText": "Perfect ''' + product.occasion + ''' Gift • Special Celebration • Thoughtful Choice",
        "styleGuide": "Celebratory atmosphere appropriate for ''' + product.occasion + ''' with festive mood and special occasion elegance",
        "layoutStructure": "Product featured as centerpiece of ''' + product.occasion + ''' celebration with appropriate decorative elements and celebratory background",
        "colorScheme": "Colors appropriate for ''' + product.occasion + ''' celebration with festive and celebratory palette choices",
        "designElements": ["celebration theme", "''' + product.occasion.lower() + ''' appropriate", "festive atmosphere", "special occasion", "gift presentation"]
      }
    }'''


# Integration instructions for services.py:
print("INTEGRATION INSTRUCTIONS:")
print("1. Replace lines 505-517 with: occasion_context = get_enhanced_occasion_prompt_section(product, tone_style, product_category)")
print("2. Replace the A+ content structure with: enhanced_aplus = get_enhanced_aplus_content_structure(product, product_category)")
print("3. Add these functions at the top of the _generate_amazon_listing method")
print("4. Update the prompt to use {occasion_context} instead of the current occasion section")
print("5. Update the aPlusContentPlan section to use the enhanced structure")