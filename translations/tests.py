"""
Test cases for the Translation endpoints
"""
from django.urls import reverse
from rest_framework.test import APITestCase


class PlainTextTranslatorTestCase(APITestCase):

    def test_that_tranlations_can_be_called_correctly(self):
        """
        The endpoint returns a status of 200 when provided with the correct
        data
        """
        url = reverse("translator-list")

        data = {
            "language_code": "pt",
            "text": "hello, how are you?"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
    
    def test_that_the_text_is_translated_successfully(self):
        url = reverse("translator-list")

        data = {
            "language_code": "pt",
            "text": "hello, how are you?"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("translated_text", response.data)