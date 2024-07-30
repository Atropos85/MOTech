from django.http import JsonResponse
from .models import APIKey

class APIKeyRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        api_key = request.headers.get('X-API-KEY')
        if not api_key:
            return JsonResponse({'error': 'API Key required'}, status=403)
        
        try:
            key = APIKey.objects.get(key=api_key, is_active=True)
            request.user = key.user
        except APIKey.DoesNotExist:
            return JsonResponse({'error': 'Invalid API Key'}, status=403)
        
        return super().dispatch(request, *args, **kwargs)