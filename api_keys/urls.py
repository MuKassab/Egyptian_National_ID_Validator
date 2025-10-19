from django.urls import path
from api_keys.views.api_key_views import GenerateApiKeyView, VerifyApiKeyView, GetUsageStatsView

urlpatterns = [
    path("generate", GenerateApiKeyView.as_view(), name="generate_api_key"),
    path("verify", VerifyApiKeyView.as_view(), name="verify_api_key"),
    path("usage-stats", GetUsageStatsView.as_view(), name="get_usage_stats"),
]