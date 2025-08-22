from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import json
import sys
import io
from .models import Product
from .serializers import ProductSerializer

@method_decorator(csrf_exempt, name='dispatch')
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        """Override create to completely bypass console output and logging"""
        import sys
        import os
        import logging
        
        # Create a null device that discards all output
        class NullDevice:
            def write(self, s): pass
            def flush(self): pass
            def close(self): pass
        
        # Store original values
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        original_logging_level = logging.root.level
        
        try:
            # Completely silence ALL output
            null_device = NullDevice()
            sys.stdout = null_device
            sys.stderr = null_device
            
            # Disable ALL logging
            logging.disable(logging.CRITICAL)
            
            # Set safe environment
            os.environ['PYTHONIOENCODING'] = 'utf-8'
            
            # Manual product creation to bypass any middleware issues
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                product = serializer.save()
                
                # Return success response manually
                return Response({
                    'id': product.id,
                    'name': product.name,
                    'brand_name': product.brand_name,
                    'target_platform': product.target_platform,
                    'created_at': product.created_at
                }, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
        except Exception as e:
            # Return minimal error response
            return Response({
                'error': 'Product creation failed',
                'details': str(e)[:100]
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        finally:
            # Restore everything
            sys.stdout = old_stdout
            sys.stderr = old_stderr
            logging.disable(logging.NOTSET)
            logging.root.setLevel(original_logging_level)

    @action(detail=False, methods=['get'])
    def test_unicode_fix(self, request):
        """Test endpoint to verify Unicode fix is active"""
        return Response({
            'message': 'Unicode fix is ACTIVE',
            'version': 'v2_null_output',
            'timestamp': '2025-07-27_13:50:00'
        })

    @action(detail=False, methods=['get'])
    def platforms(self, request):
        platforms = [
            {'value': 'amazon', 'label': 'Amazon', 'icon': '🛒'},
            {'value': 'walmart', 'label': 'Walmart', 'icon': '🏪'},
            {'value': 'etsy', 'label': 'Etsy', 'icon': '🎨'},
            {'value': 'tiktok', 'label': 'TikTok Shop', 'icon': '📱'},
            {'value': 'shopify', 'label': 'Shopify', 'icon': '🛍️'},
        ]
        return Response(platforms)

    @action(detail=False, methods=['get'])
    def brand_tones(self, request):
        tones = [
            {'value': 'professional', 'label': 'Professional'},
            {'value': 'casual', 'label': 'Casual'},
            {'value': 'luxury', 'label': 'Luxury'},
            {'value': 'playful', 'label': 'Playful'},
            {'value': 'minimal', 'label': 'Minimal'},
            {'value': 'bold', 'label': 'Bold'},
        ]
        return Response(tones)

    @action(detail=False, methods=['post'])
    def create_safe(self, request):
        """Safe product creation that handles Unicode issues"""
        import sys
        import io
        
        # Temporarily disable stdout redirection for debugging
        # old_stdout = sys.stdout
        # old_stderr = sys.stderr
        # sys.stdout = io.StringIO()
        # sys.stderr = io.StringIO()
        
        try:
            # Get request data
            data = request.data
            
            # Create user if needed
            from django.contrib.auth.models import User
            user, created = User.objects.get_or_create(
                username='demo_user',
                defaults={'email': 'demo@listory.ai', 'first_name': 'Demo', 'last_name': 'User'}
            )
            
            # Smart brand tone detection for Etsy
            brand_tone = data.get('brand_tone', '')
            target_platform = data.get('target_platform', 'amazon')
            
            # Debug print statements
            print(f"DEBUG: brand_tone from request: '{brand_tone}'")
            print(f"DEBUG: target_platform from request: '{target_platform}'")
            
            # Auto-detect brand tone for Etsy if not provided
            if not brand_tone and target_platform == 'etsy':
                brand_tone = self._auto_detect_etsy_brand_tone(data)
                print(f"DEBUG: Auto-detected brand_tone: '{brand_tone}'")
            elif not brand_tone:
                brand_tone = 'professional'  # Default for other platforms
                print(f"DEBUG: Using default brand_tone: '{brand_tone}'")
            
            # Auto-set marketplace for Etsy
            marketplace = data.get('marketplace', '')
            if target_platform == 'etsy' and not marketplace:
                marketplace = 'etsy'
                print(f"DEBUG: Auto-set marketplace to: '{marketplace}'")
            elif not marketplace:
                marketplace = 'us'  # Default for other platforms
                print(f"DEBUG: Using default marketplace: '{marketplace}'")
            
            # Create product directly with all fields
            product = Product.objects.create(
                user=user,
                name=data.get('name', ''),
                description=data.get('description', ''),
                brand_name=data.get('brand_name', ''),
                brand_tone=brand_tone,
                target_platform=target_platform,
                marketplace=marketplace,
                marketplace_language=data.get('marketplace_language', 'en'),
                competitor_urls=data.get('competitor_urls', ''),
                price=data.get('price'),
                categories=data.get('categories', ''),
                features=data.get('features', ''),
                target_keywords=data.get('target_keywords', ''),
                occasion=data.get('occasion', ''),
                seo_keywords=data.get('seo_keywords', ''),
                long_tail_keywords=data.get('long_tail_keywords', ''),
                faqs=data.get('faqs', ''),
                whats_in_box=data.get('whats_in_box', ''),
                product_urls=data.get('product_urls', ''),
                competitor_asins=data.get('competitor_asins', ''),
                brand_persona=data.get('brand_persona', ''),
                target_audience=data.get('target_audience', ''),
            )
            
            # Return success response with auto-detection info
            response_data = {
                'id': product.id,
                'name': product.name,
                'brand_name': product.brand_name,
                'brand_tone': product.brand_tone,
                'target_platform': product.target_platform,
                'marketplace': product.marketplace,
                'created_at': product.created_at.isoformat(),
                'status': 'created'
            }
            
            # Add auto-detection message for Etsy
            if target_platform == 'etsy' and not data.get('brand_tone', ''):
                response_data['message'] = f'Etsy product created with auto-detected brand tone: {product.brand_tone}'
            
            return Response(response_data, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({
                'error': str(e),
                'message': 'Product creation failed'
            }, status=status.HTTP_400_BAD_REQUEST)
        finally:
            # Restore stdout/stderr (commented out for debugging)
            # sys.stdout = old_stdout
            # sys.stderr = old_stderr
            pass
    
    def _auto_detect_etsy_brand_tone(self, data):
        """AI-powered brand tone detection for Etsy products"""
        name = data.get('name', '').lower()
        description = data.get('description', '').lower()
        features = data.get('features', '').lower()
        
        combined_text = f"{name} {description} {features}"
        
        # Keywords mapping for automatic detection based on 2025 Etsy research
        tone_keywords = {
            'handmade_artisan': ['handmade', 'artisan', 'crafted', 'handcrafted', 'made by hand', 'craft'],
            'vintage_charm': ['vintage', 'retro', 'antique', 'classic', 'timeless', 'nostalgic'],
            'bohemian_free': ['bohemian', 'boho', 'free spirit', 'wanderlust', 'hippie', 'eclectic'],
            'cottagecore_cozy': ['cottage', 'cozy', 'farmhouse', 'rustic', 'country', 'pastoral'],
            'modern_minimalist': ['minimal', 'clean', 'simple', 'geometric', 'sleek', 'contemporary'],
            'whimsical_playful': ['whimsical', 'playful', 'fun', 'quirky', 'cute', 'magical'],
            'eco_conscious': ['eco', 'sustainable', 'organic', 'natural', 'bamboo', 'recycled'],
            'luxury_handcrafted': ['luxury', 'premium', 'high-end', 'elegant', 'sophisticated'],
            'artistic_creative': ['artistic', 'creative', 'unique', 'original', 'expressive', 'art'],
            'messy_coquette': ['coquette', 'feminine', 'ruffles', 'bows', 'pink', 'girly'],
            'chateaucore': ['french', 'chateau', 'romantic', 'ornate', 'baroque', 'elegant'],
            'galactic_metallic': ['metallic', 'chrome', 'silver', 'holographic', 'futuristic', 'space'],
        }
        
        # Score each tone based on keyword matches
        tone_scores = {}
        for tone, keywords in tone_keywords.items():
            score = sum(1 for keyword in keywords if keyword in combined_text)
            if score > 0:
                tone_scores[tone] = score
        
        # Return the tone with highest score, or default
        if tone_scores:
            best_tone = max(tone_scores, key=tone_scores.get)
            return best_tone
        
        # Default to handmade_artisan for Etsy
        return 'handmade_artisan'


@csrf_exempt
@require_http_methods(["POST"])
def create_product_simple(request):
    """Simple product creation view that bypasses DRF to avoid Unicode issues"""
    try:
        # Redirect stdout to prevent console encoding issues
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        sys.stdout = io.StringIO()
        sys.stderr = io.StringIO()
        
        try:
            # Parse JSON data
            data = json.loads(request.body)
            
            # Create user if needed
            from django.contrib.auth.models import User
            user, created = User.objects.get_or_create(
                username='demo_user',
                defaults={'email': 'demo@listory.ai', 'first_name': 'Demo', 'last_name': 'User'}
            )
            
            # Create product
            product = Product.objects.create(
                user=user,
                name=data.get('name', ''),
                description=data.get('description', ''),
                brand_name=data.get('brand_name', ''),
                brand_tone=data.get('brand_tone', 'professional'),
                target_platform=data.get('target_platform', 'amazon'),
                competitor_urls=data.get('competitor_urls', ''),
                price=data.get('price'),
                categories=data.get('categories', ''),
                features=data.get('features', ''),
                target_keywords=data.get('target_keywords', '')
            )
            
            # Return success response
            return JsonResponse({
                'id': product.id,
                'name': product.name,
                'brand_name': product.brand_name,
                'target_platform': product.target_platform,
                'created_at': product.created_at.isoformat(),
                'status': 'created'
            }, status=201)
            
        finally:
            # Restore stdout/stderr
            sys.stdout = old_stdout
            sys.stderr = old_stderr
            
    except Exception as e:
        return JsonResponse({
            'error': str(e),
            'message': 'Product creation failed'
        }, status=400)