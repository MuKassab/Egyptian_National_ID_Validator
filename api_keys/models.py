from django.db import models

class ApiKey(models.Model):
    key_hash = models.CharField(max_length=128, unique=True)
    last_usage = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"ApiKey {self.key_hash[:8]}..."

class ApiKeyUsage(models.Model):
    api_key = models.ForeignKey(ApiKey, on_delete=models.CASCADE, related_name='usage_logs')
    endpoint = models.CharField(max_length=200)
    time_of_usage = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Usage of {self.api_key.key_hash[:8]}... at {self.endpoint}"