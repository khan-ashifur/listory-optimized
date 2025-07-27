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
        
        # Redirect stdout to prevent console encoding issues
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        sys.stdout = io.StringIO()
        sys.stderr = io.StringIO()
        
        try:
            # Get request data
            data = request.data
            
            # Create user if needed
            from django.contrib.auth.models import User
            user, created = User.objects.get_or_create(
                username='demo_user',
                defaults={'email': 'demo@listory.ai', 'first_name': 'Demo', 'last_name': 'User'}
            )
            
            # Create product directly
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
            return Response({
                'id': product.id,
                'name': product.name,
                'brand_name': product.brand_name,
                'target_platform': product.target_platform,
                'created_at': product.created_at.isoformat(),
                'status': 'created'
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({
                'error': str(e),
                'message': 'Product creation failed'
            }, status=status.HTTP_400_BAD_REQUEST)
        finally:
            # Restore stdout/stderr
            sys.stdout = old_stdout
            sys.stderr = old_stderr


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