from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json

@csrf_exempt 
@require_http_methods(["GET", "POST"])
def test_api(request):
    """Simple test endpoint to verify API is working"""
    if request.method == 'GET':
        return JsonResponse({
            'status': 'success',
            'message': '✅ API is working!',
            'method': 'GET'
        })
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body) if request.body else {}
            return JsonResponse({
                'status': 'success', 
                'message': '✅ POST request received!',
                'received_data': data
            })
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': f'Error processing POST: {str(e)}'
            }, status=400)