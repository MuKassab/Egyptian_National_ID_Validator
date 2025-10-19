from django.contrib import admin
from api_keys.models import ApiKey, ApiKeyUsage

admin.site.register(ApiKey)
admin.site.register(ApiKeyUsage)