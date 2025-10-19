from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api_keys.decorators.api_key_tracker import track_api_key_usage
from national_id.serializers.national_id_serializer import NationalIdSerializer
from national_id.services.national_id_service import NationalIdService

class NationalIdValidationViews(APIView):
    @track_api_key_usage("validate_national_id")
    def post(self, request):
        serializer = NationalIdSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        national_id = serializer.validated_data["national_id"]
        try:
            result = NationalIdService.validate_national_id(national_id)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        response = {"is_valid_national_id": result[0]}
        if not result[0]:
            response["reason"] = result[1]
            
        return Response(response, status=status.HTTP_200_OK)
