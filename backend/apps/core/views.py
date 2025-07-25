from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import Product
from .serializers import ProductSerializer


@method_decorator(csrf_exempt, name='dispatch')
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]  # Remove authentication for demo

    def get_queryset(self):
        # For demo purposes, return all products
        return Product.objects.all()
    
    def create(self, request, *args, **kwargs):
        print(f"Received product data: {request.data}")  # Debug log
        print(f"Request headers: {dict(request.headers)}")  # Debug headers
        print(f"Request method: {request.method}")  # Debug method
        try:
            serializer = self.get_serializer(data=request.data)
            print(f"Serializer valid: {serializer.is_valid()}")
            if not serializer.is_valid():
                print(f"Serializer errors: {serializer.errors}")
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as e:
            print(f"Product creation error: {e}")  # Debug log
            import traceback
            print(f"Full traceback: {traceback.format_exc()}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
    def test_create(self, request):
        """Debug endpoint to test product creation"""
        print(f"Raw request data: {request.data}")
        serializer = self.get_serializer(data=request.data)
        print(f"Serializer valid: {serializer.is_valid()}")
        if not serializer.is_valid():
            print(f"Serializer errors: {serializer.errors}")
            return Response(serializer.errors, status=400)
        return Response({"message": "Data is valid"}, status=200)