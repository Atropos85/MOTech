from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
from .models import APIKey

class APIKeyMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        api_key = request.headers.get('X-API-Key')
        if api_key:
            try:
                key = APIKey.objects.get(key=api_key, is_active=True)
                request.user = key.user

                if key.user.is_superuser:
                    # Permisos para administradores
                    pass
                else:
                    return JsonResponse({'error': 'unauthorized access'}, status=400)
            except APIKey.DoesNotExist:
                return JsonResponse({'error': 'Invalid API Key'}, status=403)
        else:
            return JsonResponse({'error': 'API Key required'}, status=400)
        
        return self.get_response(request)

