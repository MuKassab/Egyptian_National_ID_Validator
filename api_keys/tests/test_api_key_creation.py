from rest_framework.test import APITestCase
from rest_framework import status

from api_keys.helpers.key_generator import hash_api_key
from api_keys.models import ApiKey

class GenerateApiKeyTests(APITestCase):
    def test_generate_api_key(self):
        """
        Ensure the API generates a new key successfully.
        """
        url = "/api/api-keys/generate"
        response = self.client.post(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        self.assertIn("api_key", response.data)
        self.assertTrue(len(response.data["api_key"]) > 0)

        # Assert the key is 64 characters long
        self.assertEqual(len(response.data["api_key"]), 64)

        # Assert the key is alphanumeric
        self.assertTrue(response.data["api_key"].isalnum())

        hashed_key = hash_api_key(response.data["api_key"])
        self.assertTrue(ApiKey.objects.filter(key_hash=hashed_key).exists())