from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import GeneratedListing, ListingImage
from .serializers import GeneratedListingSerializer, ListingImageSerializer
from .services import ListingGeneratorService
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