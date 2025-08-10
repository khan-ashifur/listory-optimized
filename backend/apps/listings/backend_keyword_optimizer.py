"""
Backend Keywords Optimizer - Maximize Amazon Backend Search Terms
Optimizes backend keywords to use 100% of available character space efficiently
"""

import re

class BackendKeywordOptimizer:
    """Optimizes backend keywords for maximum Amazon visibility"""
    
    def __init__(self):
        # Maximum character limits per marketplace
        self.char_limits = {
            'com': 249,  # US
            'de': 249,   # Germany  
            'fr': 249,   # France
            'it': 249,   # Italy
            'es': 249,   # Spain
            'co.uk': 249 # UK
        }
        
        # French keyword enhancement patterns - Comprehensive and product-agnostic
        self.french_patterns = {
            # Universal plural forms for any product
            'plurals': {
                'planche': ['planches', 'planche'],
                'couteau': ['couteaux', 'couteau'],
                'ustensile': ['ustensiles', 'ustensile'],
                'accessoire': ['accessoires', 'accessoire'],
                'cuisine': ['cuisines', 'cuisine'],
                'cadeau': ['cadeaux', 'cadeau'],
                'produit': ['produits', 'produit'],
                'article': ['articles', 'article'],
                'outil': ['outils', 'outil'],
                'équipement': ['équipements', 'équipement'],
                'materiau': ['matériaux', 'materiau'],
                'professionnel': ['professionnels', 'professionnel'],
                'portable': ['portables', 'portable']
            },
            
            # Common French typos/no accents - Universal
            'typos': {
                'qualité': 'qualite',
                'sécurité': 'securite', 
                'efficacité': 'efficacite',
                'durabilité': 'durabilite',
                'résistant': 'resistant',
                'hygiénique': 'hygienique',
                'étanche': 'etanche',
                'étanches': 'etanches',
                'résistance': 'resistance',
                'écologique': 'ecologique',
                'ergonomique': 'ergonomique',
                'pratique': 'pratique',
                'économique': 'economique',
                'électrique': 'electrique',
                'précision': 'precision',
                'français': 'francais',
                'française': 'francaise',
                'été': 'ete'
            },
            
            # High-volume search phrases - More generic and comprehensive
            'high_volume': [
                'cuisine professionnelle',
                'ustensiles cuisine',
                'accessoires cuisine',
                'matériel cuisine',
                'équipement cuisine',
                'outils cuisine',
                'cuisine maison',
                'cuisine moderne',
                'ustensile pratique',
                'accessoire indispensable',
                'qualité professionnelle',
                'fabrication française',
                'made in france',
                'design moderne',
                'utilisation quotidienne',
                'nettoyage facile',
                'hygiène alimentaire',
                'sécurité alimentaire'
            ],
            
            # Seasonal/occasion keywords - Universal
            'occasions': [
                'cadeau noël', 'cadeau noel',
                'cadeau saint-valentin', 'cadeau valentin',
                'cadeau fête des mères', 'cadeau fete meres', 
                'cadeau fête des pères', 'cadeau fete peres',
                'cadeau anniversaire', 'cadeau mariage',
                'idée cadeau', 'idee cadeau',
                'cadeau cuisine', 'cadeau chef',
                'cadeau femme', 'cadeau homme',
                'liste mariage', 'cadeau original',
                'fêtes fin année', 'fetes fin annee'
            ],
            
            # Material conquest terms - Kitchen focused
            'materials': [
                'bambou', 'bois', 'plastique', 'inox',
                'acier inoxydable', 'titane', 'ceramique',
                'verre', 'silicone', 'caoutchouc',
                'alternative bambou', 'remplace plastique',
                'mieux que bois', 'superieur inox',
                'sans plastique', 'anti bacterien',
                'non poreux', 'durable'
            ],
            
            # Brand conquest terms - Generic competitors
            'competitor': [
                'ikea cuisine', 'tefal ustensile',
                'joseph joseph', 'oxo accessoire',
                'tupperware cuisine', 'pyrex ustensile',
                'kitchenaid accessoire', 'wmf cuisine',
                'sabatier couteau', 'global ustensile',
                'berghoff cuisine', 'ricardo ustensile',
                'mastrad accessoire', 'pradel cuisine'
            ]
        }
        
        # German keyword enhancement patterns  
        self.german_patterns = {
            'plurals': {
                'ventilator': ['ventilatoren', 'ventilator'],
                'lüfter': ['lüfter', 'lufter'],
                'geschenk': ['geschenke', 'geschenk'],
                'kühlung': ['kühlungen', 'kühlung']
            },
            
            'typos': {
                'für': 'fuer',
                'kühlung': 'kuehlung', 
                'größer': 'groesser',
                'lüfter': 'luefter',
                'büro': 'buero'
            },
            
            'high_volume': [
                'handventilator professionell',
                'mini ventilator büro', 
                'tragbarer lüfter akku',
                'ventilator ohne lärm',
                'usb ventilator leise'
            ],
            
            'occasions': [
                'geschenk weihnachten',
                'valentinstag geschenk',
                'muttertag geschenk',
                'vatertag geschenk',
                'geburtstag geschenk'
            ]
        }
    
    def optimize_backend_keywords(self, primary_keywords, marketplace='com', product_category=None):
        """Generate optimized backend keywords within character limits"""
        
        # Get character limit for marketplace
        char_limit = self.char_limits.get(marketplace, 249)
        
        # Generate enhanced keyword list
        if marketplace == 'fr':
            enhanced_keywords = self._enhance_french_keywords(primary_keywords)
        elif marketplace == 'de':
            enhanced_keywords = self._enhance_german_keywords(primary_keywords)
        else:
            enhanced_keywords = primary_keywords  # Keep US/other markets as is
        
        # Optimize for space efficiency
        optimized_keywords = self._optimize_for_space(enhanced_keywords, char_limit)
        
        return optimized_keywords
    
    def _enhance_french_keywords(self, base_keywords):
        """Enhance French keywords with patterns - prioritize base keywords"""
        enhanced = set()
        
        # First, ensure base keywords are preserved (highest priority)
        for keyword in base_keywords:
            enhanced.add(keyword.strip().lower())
        
        # Add typo variants of base keywords (critical for coverage)
        base_with_typos = set(base_keywords)
        for keyword in base_keywords:
            typo_variant = keyword.lower()
            for accented, unaccented in self.french_patterns['typos'].items():
                typo_variant = typo_variant.replace(accented, unaccented)
            if typo_variant != keyword.lower():
                base_with_typos.add(typo_variant)
        enhanced.update(base_with_typos)
        
        # Add plural forms of base keywords
        for base_keyword in base_keywords:
            for singular, plurals in self.french_patterns['plurals'].items():
                if singular in base_keyword.lower():
                    for plural in plurals:
                        enhanced.add(base_keyword.lower().replace(singular, plural))
        
        # Add material conquest terms (bambou, plastique, inox, etc.) - HIGH PRIORITY
        enhanced.update(self.french_patterns['materials'])  # Use all materials for max conquest
        
        # Add seasonal keywords (limited set to save space)
        seasonal_priority = ['cadeau noël', 'cadeau noel', 'cadeau', 'idée cadeau', 'idee cadeau', 'cadeau cuisine', 'fête', 'noël']
        enhanced.update(seasonal_priority)
        
        # Add high-volume phrases (limited)
        high_vol_priority = ['cuisine professionnelle', 'ustensiles cuisine', 'qualité professionnelle', 'made in france', 'français', 'française']
        enhanced.update(high_vol_priority)
        
        # Add competitor conquest terms (limited)
        competitor_priority = ['ikea cuisine', 'tefal ustensile', 'joseph joseph']
        enhanced.update(competitor_priority)
        
        # Clean and deduplicate
        return list(self._clean_keywords(enhanced))
    
    def _enhance_german_keywords(self, base_keywords):
        """Enhance German keywords with patterns"""
        enhanced = set(base_keywords)
        
        # Add plural forms
        for base_keyword in base_keywords:
            for singular, plurals in self.german_patterns['plurals'].items():
                if singular in base_keyword.lower():
                    for plural in plurals:
                        enhanced.add(base_keyword.lower().replace(singular, plural))
        
        # Add typo variants (no umlauts)
        for keyword in list(enhanced):
            typo_variant = keyword
            for umlaut, no_umlaut in self.german_patterns['typos'].items():
                typo_variant = typo_variant.replace(umlaut, no_umlaut)
            if typo_variant != keyword:
                enhanced.add(typo_variant)
        
        # Add high-volume phrases
        enhanced.update(self.german_patterns['high_volume'])
        
        # Add seasonal keywords
        enhanced.update(self.german_patterns['occasions'])
        
        return list(self._clean_keywords(enhanced))
    
    def _clean_keywords(self, keywords):
        """Clean and deduplicate keywords"""
        cleaned = set()
        
        for keyword in keywords:
            if not keyword or len(keyword.strip()) < 3:
                continue
                
            # Clean the keyword
            clean_keyword = keyword.strip().lower()
            clean_keyword = re.sub(r'[^\w\sàáâäçèéêëìíîïñòóôöùúûü-]', '', clean_keyword)
            clean_keyword = re.sub(r'\s+', ' ', clean_keyword).strip()
            
            if len(clean_keyword) >= 3:
                cleaned.add(clean_keyword)
        
        return cleaned
    
    def _optimize_for_space(self, keywords, char_limit):
        """Optimize keyword list to maximize character usage with smart prioritization"""
        
        # Remove duplicates and semantic duplicates
        unique_keywords = list(set(keywords))
        
        # Remove substring duplicates (if "cuisine" exists, remove "cuisines" to save space)
        filtered_keywords = []
        unique_keywords.sort(key=len)  # Process shortest first
        
        for keyword in unique_keywords:
            # Check if this keyword is a substring of any already added keyword
            is_duplicate = False
            for existing in filtered_keywords:
                if keyword in existing or existing in keyword:
                    # Keep the shorter version unless the longer has significantly more value
                    if len(keyword) <= len(existing):
                        # Remove the longer version and add the shorter
                        if existing in filtered_keywords:
                            filtered_keywords.remove(existing)
                        filtered_keywords.append(keyword)
                        is_duplicate = True
                        break
                    else:
                        is_duplicate = True
                        break
            
            if not is_duplicate:
                filtered_keywords.append(keyword)
        
        # Prioritize keywords by value (base keywords > conquest terms > seasonal > generic)
        critical_priority = []  # Base keywords with accents
        high_priority = []      # Conquest terms
        medium_priority = []    # Seasonal terms  
        low_priority = []       # Generic terms
        
        french_accents = ['é', 'è', 'à', 'ç', 'ù', 'â', 'ê', 'î', 'ô', 'û']
        conquest_terms = ['bambou', 'plastique', 'inox', 'bois', 'alternative', 'mieux', 'superieur', 'remplace']
        seasonal_terms = ['cadeau', 'noel', 'noël', 'valentin', 'mariage', 'fete', 'fête']
        
        for keyword in filtered_keywords:
            # Critical: Keywords with French accents (preserve these!)
            if any(char in keyword for char in french_accents):
                critical_priority.append(keyword)
            # High: Conquest terms
            elif any(term in keyword.lower() for term in conquest_terms):
                high_priority.append(keyword)
            # Medium: Seasonal terms
            elif any(term in keyword.lower() for term in seasonal_terms):
                medium_priority.append(keyword)
            # Low: Generic terms
            else:
                low_priority.append(keyword)
        
        # Sort each priority group by length (shortest first for max coverage)
        critical_priority.sort(key=len)
        high_priority.sort(key=len)
        medium_priority.sort(key=len)
        low_priority.sort(key=len)
        
        # Build optimized string prioritizing high-value terms
        optimized_parts = []
        current_length = 0
        
        # Process in order: critical (accents) > conquest terms > seasonal > generic
        for priority_group in [critical_priority, high_priority, medium_priority, low_priority]:
            for keyword in priority_group:
                # Calculate length including comma separator
                keyword_length = len(keyword)
                separator_length = 2 if optimized_parts else 0  # ", " or ""
                total_addition = keyword_length + separator_length
                
                # Add keyword if it fits
                if current_length + total_addition <= char_limit:
                    optimized_parts.append(keyword)
                    current_length += total_addition
        
        # Join with commas and return
        result = ", ".join(optimized_parts)
        
        # Ensure we're within limit
        if len(result) > char_limit:
            # Trim to fit
            result = result[:char_limit-3] + "..."
            # Remove incomplete word at end
            last_comma = result.rfind(',')
            if last_comma > 0:
                result = result[:last_comma]
        
        return result
    
    def analyze_keyword_efficiency(self, backend_keywords, char_limit=249):
        """Analyze backend keyword efficiency"""
        
        if not backend_keywords:
            return {
                "current_length": 0,
                "char_limit": char_limit,
                "usage_percentage": 0,
                "keywords_count": 0,
                "efficiency": "Empty"
            }
        
        current_length = len(backend_keywords)
        usage_percentage = (current_length / char_limit) * 100
        keywords_count = len(backend_keywords.split(','))
        
        if usage_percentage >= 95:
            efficiency = "Excellent"
        elif usage_percentage >= 80:
            efficiency = "Good" 
        elif usage_percentage >= 60:
            efficiency = "Fair"
        else:
            efficiency = "Poor"
        
        return {
            "current_length": current_length,
            "char_limit": char_limit,
            "usage_percentage": usage_percentage,
            "keywords_count": keywords_count,
            "efficiency": efficiency,
            "wasted_chars": char_limit - current_length
        }