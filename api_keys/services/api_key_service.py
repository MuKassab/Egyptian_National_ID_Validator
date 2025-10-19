from api_keys.models import ApiKey, ApiKeyUsage
from api_keys.helpers.key_generator import generate_api_key, hash_api_key
from datetime import datetime

class ApiKeyService:
    """
    Service class for API key operations.
    """
    
    @staticmethod
    def generate_api_key() -> dict:
        """
        Generate a new API key and store its hash.
        Always generates a 64-character API key.
        
        Returns:
            dict: Dictionary containing the generated API key and status
        """
        try:
            api_key = generate_api_key()
            
            key_hash = hash_api_key(api_key)
            
            # Check if hash already exists (very unlikely but possible)
            if ApiKey.objects.filter(key_hash=key_hash).exists():
                return ApiKeyService.generate_api_key()
            
            # Create and save the API key record
            api_key_obj = ApiKey.objects.create(key_hash=key_hash)
            
            return {
                "success": True,
                "api_key": api_key,
                "message": "API key generated successfully"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to generate API key: {str(e)}"
            }
    
    @staticmethod
    def verify_api_key(api_key: str) -> dict:
        """
        Verify an API key against stored hashes.
        
        Args:
            api_key (str): The API key to verify
            
        Returns:
            dict: Verification result
        """
        try:
            key_hash = hash_api_key(api_key)
            api_key_obj = ApiKey.objects.get(key_hash=key_hash, is_active=True)
            
            # Update last usage
            api_key_obj.last_usage = datetime.now()
            api_key_obj.save(update_fields=['last_usage'])
            
            return {
                "valid": True,
                "id": api_key_obj.id,
                "last_usage": api_key_obj.last_usage
            }
            
        except ApiKey.DoesNotExist:
            return {
                "valid": False,
                "error": "Invalid API key"
            }
        except Exception as e:
            return {
                "valid": False,
                "error": f"Verification failed: {str(e)}"
            }
    
    @staticmethod
    def track_usage(api_key: str, endpoint: str) -> dict:
        """
        Track API key usage for analytics and monitoring.
        
        Args:
            api_key (str): The API key that was used
            endpoint (str): The endpoint that was accessed
            
        Returns:
            dict: Tracking result
        """
        try:
            ApiKeyService.verify_api_key(api_key)

            key_hash = hash_api_key(api_key)
            api_key_obj = ApiKey.objects.get(key_hash=key_hash, is_active=True)
            
            # Create usage log
            ApiKeyUsage.objects.create(
                api_key=api_key_obj,
                endpoint=endpoint
            )
            
            # Update last usage timestamp
            api_key_obj.last_usage = datetime.now()
            api_key_obj.save(update_fields=['last_usage'])
            
            return {
                "success": True,
                "message": "Usage tracked successfully"
            }
            
        except ApiKey.DoesNotExist:
            return {
                "success": False,
                "error": "API key not found"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to track usage: {str(e)}"
            }
    
    @staticmethod
    def get_usage_stats(api_key: str) -> dict:
        """
        Get usage statistics for an API key.
        
        Args:
            api_key (str): The API key to get stats for
            
        Returns:
            dict: Usage statistics
        """
        try:
            key_hash = hash_api_key(api_key)
            api_key_obj = ApiKey.objects.get(key_hash=key_hash)
            
            # Get usage logs
            usage_logs = ApiKeyUsage.objects.filter(api_key=api_key_obj).order_by('-time_of_usage')
            
            # Count total usage
            total_usage = usage_logs.count()
            
            # Get recent usage (last 24 hours)
            from datetime import timedelta
            recent_cutoff = datetime.now() - timedelta(hours=24)
            recent_usage = usage_logs.filter(time_of_usage__gte=recent_cutoff).count()
            
            # Get endpoint breakdown
            endpoint_stats = {}
            for log in usage_logs:
                endpoint = log.endpoint
                endpoint_stats[endpoint] = endpoint_stats.get(endpoint, 0) + 1
            
            return {
                "success": True,
                "api_key_id": api_key_obj.id,
                "total_usage": total_usage,
                "recent_usage_24h": recent_usage,
                "endpoint_breakdown": endpoint_stats,
                "last_usage": api_key_obj.last_usage,
            }
            
        except ApiKey.DoesNotExist:
            return {
                "success": False,
                "error": "API key not found"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to get usage stats: {str(e)}"
            }