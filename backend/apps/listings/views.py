from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import GeneratedListing, ListingImage
from .serializers import (GeneratedListingSerializer, ListingImageSerializer, 
                         QualityValidationInputSerializer, QualityValidationOutputSerializer)
from .services import ListingGeneratorService
from .quality_validator import ListingQualityValidator
from apps.users.models import UserProfile


@method_decorator(csrf_exempt, name='dispatch')
class GeneratedListingViewSet(viewsets.ModelViewSet):
    queryset = GeneratedListing.objects.all()
    serializer_class = GeneratedListingSerializer
    permission_classes = [AllowAny]  # Remove authentication for demo

    def get_queryset(self):
        # For demo purposes, return all listings
        return GeneratedListing.objects.all()

    def generate(self, request, product_id=None, platform=None):
        import logging
        logger = logging.getLogger(__name__)
        logger.info(f"GENERATE REQUEST: product_id={product_id}, platform={platform}")
        logger.info(f"Request method: {request.method}")
        logger.info(f"Request path: {request.path}")
        
        try:
            if not product_id or not platform:
                return Response(
                    {'error': 'Both product_id and platform are required'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Convert product_id to integer
            try:
                product_id = int(product_id)
            except (ValueError, TypeError):
                return Response(
                    {'error': 'Invalid product_id format'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            logger.info(f"Final params: product_id={product_id}, platform={platform}")
            
            # For demo purposes, skip credit check
            # Generate listing
            logger.info("Creating service...")
            service = ListingGeneratorService()
            logger.info("Service initialized, generating listing...")
            
            logger.info(f"About to call generate_listing({product_id}, '{platform}')")
            listing = service.generate_listing(product_id, platform)
            logger.info(f"Listing generated successfully: {listing.id}")
            
            # Test: return simple response first to check if serialization is the issue
            try:
                serializer = self.get_serializer(listing)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as serialization_error:
                logger.error(f"Serialization failed: {serialization_error}")
                # Return minimal response to confirm listing was created
                return Response({
                    'id': listing.id,
                    'status': 'created',
                    'message': 'Listing generated but serialization failed due to encoding issues'
                }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            logger.error(f"Error in generate view: {e}")
            logger.error(f"Error type: {type(e)}")
            import traceback
            logger.error(f"Full traceback: {traceback.format_exc()}")
            
            # Return specific error information
            error_msg = str(e)
            if "Invalid argument" in error_msg:
                error_msg = f"OS Error: {error_msg}. This may be related to file system or network operations."
            
            return Response(
                {'error': error_msg, 'details': traceback.format_exc()},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['get'])
    def test_openai(self, request):
        """Test OpenAI connection"""
        service = ListingGeneratorService()
        if service.client:
            return Response({
                'status': 'success',
                'message': '[SUCCESS] OpenAI is properly configured and ready!',
                'ai_enabled': True
            })
        else:
            return Response({
                'status': 'error', 
                'message': '[ERROR] OpenAI not configured. Please set your API key in .env file',
                'ai_enabled': False
            }, status=400)
    
    @action(detail=True, methods=['get'])
    def images(self, request, pk=None):
        """Get image generation status for a listing"""
        listing = self.get_object()
        images = listing.images.all()
        serializer = ListingImageSerializer(images, many=True)
        
        # Calculate overall status
        total_images = images.count()
        completed_images = images.filter(status='completed').count()
        failed_images = images.filter(status='failed').count()
        
        return Response({
            'images': serializer.data,
            'summary': {
                'total': total_images,
                'completed': completed_images,
                'failed': failed_images,
                'in_progress': total_images - completed_images - failed_images,
                'all_completed': total_images > 0 and completed_images == total_images
            }
        })
    
    @action(detail=True, methods=['post'])
    def regenerate_images(self, request, pk=None):
        """Regenerate failed images for a listing"""
        listing = self.get_object()
        
        try:
            # Import here to avoid circular imports
            from .image_service import generate_listing_image, ImageGenerationService, CELERY_AVAILABLE
            
            # Find failed images and requeue them
            failed_images = listing.images.filter(status='failed')
            requeued_count = 0
            
            if CELERY_AVAILABLE:
                for image in failed_images:
                    image.status = 'pending'
                    image.save()
                    generate_listing_image.delay(image.id)
                    requeued_count += 1
            else:
                # Generate synchronously if Celery not available
                service = ImageGenerationService()
                for image in failed_images:
                    image.status = 'pending'
                    image.save()
                    service.generate_image(image.id)
                    requeued_count += 1
            
            return Response({
                'status': 'success',
                'message': f'Requeued {requeued_count} failed images for regeneration'
            })
            
        except Exception as e:
            return Response({
                'status': 'error',
                'message': f'Error regenerating images: {str(e)}'
            }, status=400)
    
    @action(detail=True, methods=['post'])
    def generate_images(self, request, pk=None):
        """Trigger image generation for a listing"""
        listing = self.get_object()
        
        try:
            from .services import ListingGeneratorService
            service = ListingGeneratorService()
            service._queue_image_generation(listing)
            
            return Response({
                'status': 'success',
                'message': 'Image generation started'
            })
            
        except Exception as e:
            return Response({
                'status': 'error',
                'message': f'Error starting image generation: {str(e)}'
            }, status=400)
    
    @action(detail=False, methods=['post'])
    def validate_quality(self, request):
        """
        Validate listing content for 10/10 emotional, conversion-focused quality.
        
        Expects JSON payload with:
        - title (required): Product title
        - bullet_points (optional): Bullet point content
        - long_description (optional): Product description
        - faqs (optional): FAQ content
        
        Returns comprehensive quality report with scores and improvement suggestions.
        """
        try:
            # Validate input data
            input_serializer = QualityValidationInputSerializer(data=request.data)
            if not input_serializer.is_valid():
                return Response({
                    'error': 'Invalid input data',
                    'details': input_serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Perform quality validation
            validator = ListingQualityValidator()
            quality_report = validator.get_validation_json(input_serializer.validated_data)
            
            # Serialize and return results
            output_serializer = QualityValidationOutputSerializer(data=quality_report)
            if output_serializer.is_valid():
                return Response({
                    'status': 'success',
                    'message': 'Quality validation completed',
                    'validation_report': output_serializer.validated_data
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'status': 'error',
                    'message': 'Error formatting validation results',
                    'raw_report': quality_report
                }, status=status.HTTP_200_OK)
                
        except Exception as e:
            return Response({
                'status': 'error',
                'message': f'Quality validation failed: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=True, methods=['get'])
    def quality_report(self, request, pk=None):
        """Get quality validation report for an existing listing."""
        try:
            listing = self.get_object()
            
            # Prepare listing data for validation
            validation_data = {
                'title': listing.title or '',
                'bullet_points': listing.bullet_points or '',
                'long_description': listing.long_description or '',
                'faqs': listing.faqs or ''
            }
            
            # Perform validation
            validator = ListingQualityValidator()
            quality_report = validator.get_validation_json(validation_data)
            
            # Include stored scores if available
            if hasattr(listing, 'quality_score') and listing.quality_score:
                quality_report['stored_scores'] = {
                    'quality_score': listing.quality_score,
                    'emotion_score': listing.emotion_score,
                    'conversion_score': listing.conversion_score,
                    'trust_score': listing.trust_score
                }
            
            return Response({
                'status': 'success',
                'listing_id': listing.id,
                'validation_report': quality_report
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'status': 'error',
                'message': f'Error generating quality report: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@require_http_methods(["POST"])
def generate_listing_clean(request, product_id, platform):
    """
    Clean API endpoint that bypasses DRF serialization issues.
    Returns minimal JSON response to prevent encoding errors.
    """
    try:
        # Convert product_id to integer
        try:
            product_id = int(product_id)
        except (ValueError, TypeError):
            return JsonResponse({
                'error': 'Invalid product_id format'
            }, status=400)
        
        # Generate listing using the working service
        service = ListingGeneratorService()
        listing = service.generate_listing(product_id, platform)
        
        # Return minimal response with safe encoding
        return JsonResponse({
            'success': True,
            'id': listing.id,
            'title': listing.title[:100] if listing.title else '',
            'status': listing.status,
            'aplus_length': len(listing.amazon_aplus_content) if listing.amazon_aplus_content else 0,
            'message': 'Listing generated successfully'
        }, status=201)
        
    except Exception as e:
        # Return error without traceback to avoid encoding issues
        return JsonResponse({
            'success': False,
            'error': str(e)[:200]  # Limit error message length
        }, status=500)