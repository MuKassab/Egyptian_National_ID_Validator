from functools import wraps
from django.http import JsonResponse
from django.core.cache import cache
import time

def rate_limit_by_api_key(requests_per_minute=2):
    """
    Decorator to rate limit API requests based on API key.
    Only applies rate limiting when API key header exists.
    
    Args:
        requests_per_minute (int): Maximum number of requests allowed per minute
        
    Usage:
        @rate_limit_by_api_key(requests_per_minute=2)
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

            # Get API key from headers
            api_key = request.headers.get("X-API-Key") or request.META.get("HTTP_X_API_KEY")
            
            # Only apply rate limiting if API key exists
            if api_key:
                # Create a unique cache key for this API key
                cache_key = f"rate_limit:{api_key}"
                
                # Get current request count and timestamp
                current_data = cache.get(cache_key, {"count": 0, "window_start": time.time()})
                current_time = time.time()
                
                # Check if we're still in the same minute window
                if current_time - current_data["window_start"] < 60:
                    # Still in the same minute window
                    if current_data["count"] >= requests_per_minute:
                        # Rate limit exceeded
                        return JsonResponse(
                            {
                                "error": "Rate limit exceeded",
                                "message": f"Maximum {requests_per_minute} requests per minute allowed",
                                "retry_after": 60 - int(current_time - current_data["window_start"])
                            },
                            status=429
                        )
                    else:
                        # Increment counter
                        current_data["count"] += 1
                else:
                    # New minute window, reset counter
                    current_data = {"count": 1, "window_start": current_time}
                
                # Update cache with new data (expire after 60 seconds)
                cache.set(cache_key, current_data, 60)

            # Call the original view function
            return view_func(*args, **kwargs)

        return wrapper
    return decorator
