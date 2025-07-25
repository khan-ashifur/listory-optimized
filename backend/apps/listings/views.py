from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import GeneratedListing
from .serializers import GeneratedListingSerializer
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

    @action(detail=False, methods=['post'])
    def generate(self, request, product_id=None, platform=None):
        try:
            # For demo purposes, skip credit check
            # Generate listing
            service = ListingGeneratorService()
            listing = service.generate_listing(product_id, platform)
            
            serializer = self.get_serializer(listing)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=False, methods=['get'])
    def test_openai(self, request):
        """Test OpenAI connection"""
        service = ListingGeneratorService()
        if service.client:
            return Response({
                'status': 'success',
                'message': '✅ OpenAI is properly configured and ready!',
                'ai_enabled': True
            })
        else:
            return Response({
                'status': 'error', 
                'message': '❌ OpenAI not configured. Please set your API key in .env file',
                'ai_enabled': False
            }, status=400)