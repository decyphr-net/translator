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
        """
        After the call to the API has been, and everything was successful, the
        translated text is returned
        """
        url = reverse("translator-list")

        data = {
            "language_code": "pt",
            "text": "hello, how are you?"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("translated_text", response.data)
    
    def test_error_is_thrown_if_the_language_code_is_not_provided(self):
        """
        If a language code is not present in the post data then an error
        message will be returned to the client
        """
        url = reverse("translator-list")
        data = {
            "text": "hello, how are you?"
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.data["language_code"][0], "This field is required.")
    
    def test_error_is_thrown_if_the_language_code_is_too_short(self):
        """
        If a language code is too short an error will be thrown
        """
        url = reverse("translator-list")
        data = {
            "language_code": "p",
            "text": "hello, how are you?"
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.data["language_code"][0],
            "The language code provided is too short. Please ensure the code is in ISO 639-1 format")
    
    def test_error_is_thrown_if_the_language_code_is_too_long(self):
        """
        If a language code is too long an error will be thrown
        """
        url = reverse("translator-list")
        data = {
            "language_code": "pt-BR",
            "text": "hello, how are you?"
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.data["language_code"][0],
            "The language code provided is too long. Please ensure the code is in ISO 639-1 format")