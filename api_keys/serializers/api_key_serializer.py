from rest_framework import serializers

class GenerateApiKeySerializer(serializers.Serializer):
    """
    Serializer for API key generation requests.
    API keys are always generated as 64 characters.
    """
    pass

class VerifyApiKeySerializer(serializers.Serializer):
    """
    Serializer for API key verification requests.
    """
    api_key = serializers.CharField(
        max_length=64,
        min_length=64,
        help_text="The 64-character API key to verify"
    )
    
    def validate_api_key(self, value):
        """Validate the API key format."""
        if not value:
            raise serializers.ValidationError("API key is required.")
        
        # Check if it's exactly 64 characters
        if len(value) != 64:
            raise serializers.ValidationError("API key must be exactly 64 characters long.")
        
        # Check if it contains only alphanumeric characters
        if not value.isalnum():
            raise serializers.ValidationError("API key must contain only alphanumeric characters.")
        
        return value