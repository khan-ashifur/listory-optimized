from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GeneratedListingViewSet, generate_listing_clean
from .api_fix import generate_listing_fixed

router = DefaultRouter()
router.register(r'generated', GeneratedListingViewSet, basename='generated-listing')

urlpatterns = [
    path('', include(router.urls)),
    path('generate/<int:product_id>/<str:platform>/', GeneratedListingViewSet.as_view({'post': 'generate'}), name='generate-listing'),
    path('generate-fixed/<int:product_id>/<str:platform>/', generate_listing_fixed, name='generate-listing-fixed'),
    path('generate-clean/<int:product_id>/<str:platform>/', generate_listing_clean, name='generate-listing-clean'),
]