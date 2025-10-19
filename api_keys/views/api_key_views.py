from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api_keys.serializers.api_key_serializer import GenerateApiKeySerializer, VerifyApiKeySerializer
from api_keys.services.api_key_service import ApiKeyService

class GenerateApiKeyView(APIView):
    """
    View for generating new API keys.
    """
    
    def post(self, request):
        """Generate a new API key (always 64 characters)."""
        serializer = GenerateApiKeySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        result = ApiKeyService.generate_api_key()
        
        if result['success']:
            return Response(result, status=status.HTTP_201_CREATED)
        else:
            return Response(result, status=status.HTTP_400_BAD_REQUEST)

class VerifyApiKeyView(APIView):
    """
    View for verifying API keys.
    """
    
    def post(self, request):
        """Verify an API key."""
        serializer = VerifyApiKeySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        api_key = serializer.validated_data['api_key']
        result = ApiKeyService.verify_api_key(api_key)
        
        if result['valid']:
            return Response(result, status=status.HTTP_200_OK)
        else:
            return Response(result, status=status.HTTP_401_UNAUTHORIZED)

class GetUsageStatsView(APIView):
    """
    View for getting API key usage statistics.
    """
    
    def post(self, request):
        """Get usage statistics for an API key."""
        api_key = request.data.get('api_key')
        if not api_key:
            return Response(
                {"error": "API key is required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        result = ApiKeyService.get_usage_stats(api_key)
        
        if result['success']:
            return Response(result, status=status.HTTP_200_OK)
        else:
            return Response(result, status=status.HTTP_400_BAD_REQUEST)
