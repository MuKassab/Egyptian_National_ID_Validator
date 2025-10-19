from rest_framework.test import APITestCase
from rest_framework import status

from api_keys.helpers.key_generator import generate_api_key, hash_api_key
from api_keys.models import ApiKey

class VerifyApiKeyTests(APITestCase):
    def test_verify_api_key(self):
        """
        Ensure the API verifies a key successfully.
        """
        url = "/api/api-keys/verify"
        api_key = generate_api_key()
        hashed_key = hash_api_key(api_key)
        ApiKey.objects.create(key_hash=hashed_key)
        response = self.client.post(url, format="json", data={"api_key": api_key})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.assertIn("valid", response.data)
        self.assertTrue(response.data["valid"])
        self.assertIn("id", response.data)
        self.assertIn("last_usage", response.data)
        self.assertTrue(ApiKey.objects.filter(id=response.data["id"]).exists())

    def test_verify_invalid_api_key_length(self):
        """
        Ensure the API returns an error for an invalid key.
        """
        url = "/api/api-keys/verify"
        response = self.client.post(url, format="json", data={"api_key": "invalid_api_key"})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_verify_invalid_api_key_characters(self):
        """
        Ensure the API returns an error for an invalid key.
        """
        url = "/api/api-keys/verify"
        api_key = generate_api_key()
        response = self.client.post(url, format="json", data={"api_key": api_key})

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("error", response.data)
        self.assertEqual(response.data["error"], "Invalid API key")