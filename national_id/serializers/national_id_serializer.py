from rest_framework import serializers

class NationalIdSerializer(serializers.Serializer):
    national_id = serializers.CharField()

    def validate_national_id(self, value: str) -> str:
        if not value.isdigit():
            raise serializers.ValidationError("National ID must contain digits only.")

        if len(value) != 14:
            raise serializers.ValidationError("National ID must be exactly 14 digits long.")
            
        if not value.startswith(("2", "3")):
            raise serializers.ValidationError("National ID must start with 2 or 3.")
            
        return value
