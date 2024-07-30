from django.http import JsonResponse
from .models import APIKey

def api_key_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        api_key = request.headers.get('X-API-KEY')
        if not api_key:
            return JsonResponse({'error': 'API Key required'}, status=403)
        
        try:
            key = APIKey.objects.get(key=api_key, is_active=True)
            request.user = key.user
        except APIKey.DoesNotExist:
            return JsonResponse({'error': 'Invalid API Key'}, status=403)
        
        return view_func(request, *args, **kwargs)
    return _wrapped_view