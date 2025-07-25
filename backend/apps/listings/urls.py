from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GeneratedListingViewSet

router = DefaultRouter()
router.register(r'generated', GeneratedListingViewSet, basename='generated-listing')

urlpatterns = [
    path('', include(router.urls)),
    path('generate/<int:product_id>/<str:platform>/', GeneratedListingViewSet.as_view({'post': 'generate'}), name='generate-listing'),
]