"""
Test cases for the Translation endpoints
"""
from django.urls import reverse
from rest_framework.test import APITestCase


class FullTranslationTestCase(APITestCase):

    def test_that_tranlations_can_be_called_correctly(self):
        """
        The endpoint returns a status of 200 when provided with the correct
        data
        """
        url = reverse("translator-list")

        data = {
            "initial_language_code": "en-US",
            "target_language_code": "pt",
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
            "initial_language_code": "en-US",
            "target_language_code": "pt",
            "text": "hello, how are you?"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("translated_text", response.data)
    
    def test_that_the_audio_location_is_provided(self):
        """
        After the call to the API has been, and everything was successful, the
        location to the audio file is returned
        """
        url = reverse("translator-list")

        data = {
            "initial_language_code": "en-US",
            "target_language_code": "pt",
            "text": "hello, how are you?"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("audio_location", response.data)

    def test_that_the_analyzed_text_is_provided(self):
        """
        After the call to the API has been, and everything was successful, the
        analyzeded text is returned
        """
        url = reverse("translator-list")

        data = {
            "initial_language_code": "en-US",
            "target_language_code": "pt",
            "text": "hello, how are you?"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("analyzed_text", response.data)
    
    def test_error_is_thrown_if_the_initial_language_code_is_not_provided(self):
        """
        If a language code is not present in the post data then an error
        message will be returned to the client
        """
        url = reverse("translator-list")
        data = {
            "target_language_code": "pt",
            "text": "hello, how are you?"
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.data["initial_language_code"][0], "This field is required.")
    
    def test_error_is_thrown_if_the_language_code_is_too_short(self):
        """
        If a language code is too short an error will be thrown
        """
        url = reverse("translator-list")
        data = {
            "initial_language_code": "e",
            "target_language_code": "pt",
            "text": "hello, how are you?"
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.data["initial_language_code"][0],
            "The language code is too short. Please use ISO 639-1 format")
    
    def test_error_is_thrown_if_the_language_code_is_too_long(self):
        """
        If a language code is too long an error will be thrown
        """
        url = reverse("translator-list")
        data = {
            "initial_language_code": "en-GBs",
            "target_language_code": "pt",
            "text": "hello, how are you?"
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.data["initial_language_code"][0],
            "The language code is too long. Please use ISO 639-1 format")
    
    def test_error_is_thrown_if_the_target_language_code_is_not_provided(self):
        """
        If a language code is not present in the post data then an error
        message will be returned to the client
        """
        url = reverse("translator-list")
        data = {
            "initial_language_code": "en-GB",
            "text": "hello, how are you?"
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.data["target_language_code"][0], "This field is required.")
    
    def test_error_is_thrown_if_the_target_language_code_is_too_short(self):
        """
        If a language code is too short an error will be thrown
        """
        url = reverse("translator-list")
        data = {
            "initial_language_code": "en-GB",
            "target_language_code": "p",
            "text": "hello, how are you?"
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.data["target_language_code"][0],
            "The language code is too short. Please use ISO 639-1 format")
    
    def test_error_is_thrown_if_the_target_language_code_is_too_long(self):
        """
        If a language code is too long an error will be thrown
        """
        url = reverse("translator-list")
        data = {
            "initial_language_code": "en-GB",
            "target_language_code": "pt-BR",
            "text": "hello, how are you?"
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.data["target_language_code"][0],
            "The language code is too long. Please use ISO 639-1 format")



class TextToTextTranslationTestCase(APITestCase):

    def test_that_tranlations_can_be_called_correctly(self):
        """
        The endpoint returns a status of 200 when provided with the correct
        data
        """
        url = reverse("text-to-text-list")

        data = {
            "target_language_code": "pt",
            "text": "hello, how are you?"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
    
    def test_that_the_text_is_translated_successfully(self):
        """
        After the call to the API has been, and everything was successful, the
        translated text is returned
        """
        url = reverse("text-to-text-list")

        data = {
            "target_language_code": "pt",
            "text": "hello, how are you?"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("translated_text", response.data)
    
    def test_error_is_thrown_if_the_target_language_code_is_not_provided(self):
        """
        If a language code is not present in the post data then an error
        message will be returned to the client
        """
        url = reverse("text-to-text-list")
        data = {
            "initial_language_code": "en-GB",
            "text": "hello, how are you?"
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.data["target_language_code"][0], "This field is required.")
    
    def test_error_is_thrown_if_the_target_language_code_is_too_short(self):
        """
        If a language code is too short an error will be thrown
        """
        url = reverse("text-to-text-list")
        data = {
            "target_language_code": "p",
            "text": "hello, how are you?"
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.data["target_language_code"][0],
            "The language code is too short. Please use ISO 639-1 format")
    
    def test_error_is_thrown_if_the_target_language_code_is_too_long(self):
        """
        If a language code is too long an error will be thrown
        """
        url = reverse("text-to-text-list")
        data = {
            "target_language_code": "pt-BR",
            "text": "hello, how are you?"
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.data["target_language_code"][0],
            "The language code is too long. Please use ISO 639-1 format")