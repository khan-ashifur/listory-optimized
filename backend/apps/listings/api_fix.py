"""
Direct API fix that bypasses problematic print statements
"""
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
import io
import sys
import contextlib

from .models import GeneratedListing
from .services import ListingGeneratorService
from apps.core.models import Product

@csrf_exempt
@require_http_methods(["POST"])
def generate_listing_fixed(request, product_id, platform):
    """Fixed version that captures all output to prevent encoding errors"""
    try:
        # Capture all stdout to prevent encoding issues
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        sys.stdout = io.StringIO()
        sys.stderr = io.StringIO()
        
        try:
            # Convert product_id to integer
            product_id = int(product_id)
            
            # Get product
            product = Product.objects.get(id=product_id)
            
            # Create listing
            listing = GeneratedListing.objects.create(
                product=product,
                platform=platform,
                status='processing'
            )
            
            # Generate content
            service = ListingGeneratorService()
            service._generate_amazon_listing(product, listing)
            
            # Update status
            listing.status = 'completed'
            listing.save()
            
            # Return success response
            return JsonResponse({
                'id': listing.id,
                'status': 'completed',
                'title': listing.title,
                'bullet_points': listing.bullet_points,
                'long_description': listing.long_description,
                'keywords': listing.keywords,
                'amazon_aplus_content': listing.amazon_aplus_content,
                'message': 'Listing generated successfully'
            })
            
        finally:
            # Restore stdout/stderr
            sys.stdout = old_stdout
            sys.stderr = old_stderr
            
    except Product.DoesNotExist:
        return JsonResponse({
            'error': f'Product with id {product_id} not found'
        }, status=404)
    except ValueError:
        return JsonResponse({
            'error': 'Invalid product_id format'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'error': f'Generation failed: {str(e)}'
        }, status=500)