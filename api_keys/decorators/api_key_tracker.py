from functools import wraps
from django.http import JsonResponse
from api_keys.services.api_key_service import ApiKeyService

def track_api_key_usage(endpoint_name):
    """
    Decorator to track API key usage for a specific endpoint.
    
    Args:
        endpoint_name (str): The name of the endpoint being accessed
        
    Usage:
        @track_api_key_usage("validate_national_id")
        def my_view(request):
            # Your view logic here
            pass
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(*args, **kwargs):
            # DRF passes (self, request, *args, **kwargs) for class-based views
            # and (request, *args, **kwargs) for function-based views
            if hasattr(args[0], "request"):
                # It's a method on a class-based view
                self = args[0]
                request = args[1]
            else:
                # It's a function-based view
                request = args[0]

            api_key = request.headers.get("X-API-Key") or request.META.get("HTTP_X_API_KEY")

            if api_key:
                try:
                    result = ApiKeyService.track_usage(api_key, endpoint_name)
                    if not result['success']:
                        return JsonResponse(
                            {"error": result['error']}, 
                            status=401
                        )
                except Exception as e:
                    print(f"Failed to track API key usage: {str(e)}")

            # Call the original view function
            return view_func(*args, **kwargs)

        return wrapper
    return decorator