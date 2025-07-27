from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse, HttpResponse

def health_check(request):
    return JsonResponse({'status': 'ok', 'message': 'Django server running'})

def favicon_view(request):
    return HttpResponse(status=204)  # No content

urlpatterns = [
    path('', health_check, name='health_check'),
    path('favicon.ico', favicon_view, name='favicon'),
    path('admin/', admin.site.urls),
    path('api/auth/', include('apps.users.urls')),
    path('api/listings/', include('apps.listings.urls')),
    path('api/core/', include('apps.core.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)