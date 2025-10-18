from django.urls import path

from national_id.views.national_id_data_extraction_views import NationalIdDataExtractionViews
from national_id.views.national_id_validation_views import NationalIdValidationViews

urlpatterns = [
    path("validate", NationalIdValidationViews.as_view(), name="validate_national_id"),
    path("extract-data", NationalIdDataExtractionViews.as_view(), name="extract_data_from_national_id"),
]