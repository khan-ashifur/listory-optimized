"""
Robust International Content Extractor
Bypasses broken JSON parser to extract complete German/French/Spanish content
Preserves all AI-generated optimization including brand tones and special occasions
"""

import re
import json
import logging

class InternationalContentExtractor:
    """Extracts complete international content without relying on broken JSON parsing"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def extract_international_content(self, ai_response_text, marketplace_lang):
        """
        Extract complete international content using advanced regex patterns
        Handles German ä,ö,ü,ß and other international characters
        """
        try:
            # Clean the response text BUT PRESERVE UMLAUTS
            cleaned_text = ai_response_text.strip()
            
            # Debug: Check if umlauts are present in input
            print(f"🔍 InternationalContentExtractor INPUT DEBUG:")
            print(f"   Contains ü: {'ü' in cleaned_text}")
            print(f"   Contains ä: {'ä' in cleaned_text}")
            print(f"   Contains ö: {'ö' in cleaned_text}")
            print(f"   Contains ß: {'ß' in cleaned_text}")
            
            # DEBUG: Check for German characters in input
            german_chars = ['ä', 'ö', 'ü', 'ß', 'Ä', 'Ö', 'Ü']
            input_german_chars = sum(cleaned_text.count(char) for char in german_chars)
            input_unicode_chars = sum(1 for char in cleaned_text if ord(char) > 127)
            self.logger.info(f"🔍 InternationalContentExtractor INPUT: {len(cleaned_text)} chars, German chars: {input_german_chars}, Unicode chars: {input_unicode_chars}")
            
            # Extract using multiple robust patterns
            result = {
                'productTitle': self._extract_title(cleaned_text),
                'bulletPoints': self._extract_bullets(cleaned_text),
                'productDescription': self._extract_description(cleaned_text),
                'seoKeywords': self._extract_keywords(cleaned_text),
                'backendKeywords': self._extract_backend_keywords(cleaned_text),
                'aPlusContentPlan': self._extract_aplus_content(cleaned_text),
                'brandSummary': self._extract_brand_summary(cleaned_text),
                'whatsInBox': self._extract_whats_in_box(cleaned_text),
                'trustBuilders': self._extract_trust_builders(cleaned_text),
                'faqs': self._extract_faqs(cleaned_text),
                'socialProof': self._extract_social_proof(cleaned_text),
                'guarantee': self._extract_guarantee(cleaned_text),
                'ppcStrategy': self._extract_ppc_strategy(cleaned_text)
            }
            
            # DEBUG: Check for German characters in output
            all_output = str(result.get('productTitle', '')) + str(result.get('productDescription', '')) + ' '.join(result.get('bulletPoints', []))
            output_german_chars = sum(all_output.count(char) for char in german_chars)
            output_unicode_chars = sum(1 for char in all_output if ord(char) > 127)
            self.logger.info(f"🔍 InternationalContentExtractor OUTPUT: {len(all_output)} chars, German chars: {output_german_chars}, Unicode chars: {output_unicode_chars}")
            
            # Validate extraction quality
            if self._validate_extraction(result, marketplace_lang):
                self.logger.info(f"✅ International content extracted successfully for {marketplace_lang}")
                return result
            else:
                self.logger.warning(f"⚠️ International extraction incomplete for {marketplace_lang}")
                return None
                
        except Exception as e:
            self.logger.error(f"❌ International content extraction failed: {e}")
            return None
    
    def _extract_title(self, text):
        """Extract product title with international characters"""
        patterns = [
            r'"productTitle":\s*"([^"]+(?:\\"[^"]*)*)"',
            r'"productTitle":\s*"(.*?)"(?=\s*[,}])',
            r'productTitle["\s]*:["\s]*(.*?)["]*(?=\s*[,}])'
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, text, re.DOTALL | re.IGNORECASE)
            for match in matches:
                title = match.group(1).replace('\\"', '"').strip()
                if len(title) > 20:  # Valid title should be substantial
                    return title
        
        return ""
    
    def _extract_bullets(self, text):
        """Extract bullet points array with international characters"""
        # Find the bulletPoints array
        bullet_patterns = [
            r'"bulletPoints":\s*\[(.*?)\]',
            r'bulletPoints["\s]*:["\s]*\[(.*?)\]'
        ]
        
        bullets = []
        for pattern in bullet_patterns:
            match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
            if match:
                bullet_content = match.group(1)
                
                # Extract individual bullets from the array
                bullet_matches = re.findall(r'"([^"]+(?:\\"[^"]*)*)"', bullet_content)
                if bullet_matches:
                    bullets = [bullet.replace('\\"', '"').strip() for bullet in bullet_matches]
                    if len(bullets) >= 3:  # Should have at least 3 bullets
                        return bullets[:5]  # Take max 5 bullets
        
        return []
    
    def _extract_description(self, text):
        """Extract product description with international characters"""
        patterns = [
            r'"productDescription":\s*"([^"]+(?:\\"[^"]*)*)"',
            r'"productDescription":\s*"(.*?)"(?=\s*[,}])',
            r'productDescription["\s]*:["\s]*(.*?)["]*(?=\s*[,}])'
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, text, re.DOTALL | re.IGNORECASE)
            for match in matches:
                description = match.group(1).replace('\\"', '"').strip()
                if len(description) > 50:  # Valid description should be substantial
                    return description
        
        return ""
    
    def _extract_keywords(self, text):
        """Extract SEO keywords structure"""
        # Try to extract the seoKeywords object
        patterns = [
            r'"seoKeywords":\s*({.*?})',
            r'seoKeywords["\s]*:["\s]*({.*?})'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
            if match:
                try:
                    keywords_obj = json.loads(match.group(1))
                    return keywords_obj
                except:
                    continue
        
        return {}
    
    def _extract_backend_keywords(self, text):
        """Extract backend keywords string"""
        patterns = [
            r'"backendKeywords":\s*"([^"]+(?:\\"[^"]*)*)"',
            r'backendKeywords["\s]*:["\s]*"(.*?)"'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
            if match:
                keywords = match.group(1).replace('\\"', '"').strip()
                return keywords
        
        return ""
    
    def _extract_aplus_content(self, text):
        """Extract A+ content plan structure"""
        patterns = [
            r'"aPlusContentPlan":\s*({.*?})',
            r'aPlusContentPlan["\s]*:["\s]*({.*?})'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
            if match:
                try:
                    aplus_obj = json.loads(match.group(1))
                    return aplus_obj
                except:
                    continue
        
        return {}
    
    def _extract_brand_summary(self, text):
        """Extract brand summary"""
        patterns = [
            r'"brandSummary":\s*"([^"]+(?:\\"[^"]*)*)"',
            r'brandSummary["\s]*:["\s]*"(.*?)"'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
            if match:
                summary = match.group(1).replace('\\"', '"').strip()
                return summary
        
        return ""
    
    def _extract_whats_in_box(self, text):
        """Extract what's in box content"""
        patterns = [
            r'"whatsInBox":\s*\[(.*?)\]',
            r'whatsInBox["\s]*:["\s]*\[(.*?)\]'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
            if match:
                items = re.findall(r'"([^"]+)"', match.group(1))
                return items
        
        return []
    
    def _extract_trust_builders(self, text):
        """Extract trust builders content"""
        patterns = [
            r'"trustBuilders":\s*\[(.*?)\]',
            r'trustBuilders["\s]*:["\s]*\[(.*?)\]'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
            if match:
                items = re.findall(r'"([^"]+)"', match.group(1))
                return items
        
        return []
    
    def _extract_faqs(self, text):
        """Extract FAQs content"""
        patterns = [
            r'"faqs":\s*\[(.*?)\]',
            r'faqs["\s]*:["\s]*\[(.*?)\]'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
            if match:
                items = re.findall(r'"([^"]+)"', match.group(1))
                return items
        
        return []
    
    def _extract_social_proof(self, text):
        """Extract social proof content"""
        patterns = [
            r'"socialProof":\s*"([^"]+(?:\\"[^"]*)*)"',
            r'socialProof["\s]*:["\s]*"(.*?)"'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
            if match:
                proof = match.group(1).replace('\\"', '"').strip()
                return proof
        
        return ""
    
    def _extract_guarantee(self, text):
        """Extract guarantee content"""
        patterns = [
            r'"guarantee":\s*"([^"]+(?:\\"[^"]*)*)"',
            r'guarantee["\s]*:["\s]*"(.*?)"'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
            if match:
                guarantee = match.group(1).replace('\\"', '"').strip()
                return guarantee
        
        return ""
    
    def _extract_ppc_strategy(self, text):
        """Extract PPC strategy structure"""
        patterns = [
            r'"ppcStrategy":\s*({.*?})',
            r'ppcStrategy["\s]*:["\s]*({.*?})'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
            if match:
                try:
                    ppc_obj = json.loads(match.group(1))
                    return ppc_obj
                except:
                    continue
        
        return {}
    
    def _validate_extraction(self, result, marketplace_lang):
        """Validate that extraction captured substantial content"""
        # Check essential fields
        title_ok = len(result.get('productTitle', '')) > 50
        bullets_ok = len(result.get('bulletPoints', [])) >= 3
        description_ok = len(result.get('productDescription', '')) > 100
        
        # Check for international characters if applicable
        all_text = str(result.get('productTitle', '')) + str(result.get('productDescription', ''))
        has_intl_chars = any(ord(char) > 127 for char in all_text) if marketplace_lang != 'en' else True
        
        quality_score = sum([title_ok, bullets_ok, description_ok, has_intl_chars])
        
        self.logger.info(f"International extraction quality: {quality_score}/4")
        self.logger.info(f"  Title: {'✅' if title_ok else '❌'} ({len(result.get('productTitle', ''))} chars)")
        self.logger.info(f"  Bullets: {'✅' if bullets_ok else '❌'} ({len(result.get('bulletPoints', []))} bullets)")
        self.logger.info(f"  Description: {'✅' if description_ok else '❌'} ({len(result.get('productDescription', ''))} chars)")
        self.logger.info(f"  Intl chars: {'✅' if has_intl_chars else '❌'}")
        
        return quality_score >= 3  # Need at least 3/4 for success