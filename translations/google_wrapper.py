"""
The Google wrapper class is a mixin that will be used in all of the endpoints
relating to the interaction with Google Cloud services.
"""
from django.conf import settings
from google.cloud import translate


class GoogleMixin:
    """Google Cloud Mixin Class

    This mixin will contain all of the necessary functionality required to
    integrate with the relevant Google Cloud services.

    Examples:
        In order to take advantage of this mixin, simple extended it::
            class TranslationEndpoint(viewsets.ViewSet, GoogleMixin):
    """
    translation_client = translate.TranslationServiceClient()
    parent = translation_client.location_path(
        settings.GOOGLE_PROJECT, "global")
    
    def translate_text(self, target_language_code, text):
        """Translate Text

        The interface into Google's Translation API.

        Args:
            target_language_code : A ISO 639-1 code that will be used to \
            inform Google Translate of the target language
            text (str): The text that is needed to be translated
        
        Returns:
            Tranlated text (str): The text that was returned by the Google Translate API
        
        Examples:
            translated_text = self.translate_text(language_code, text)
        """
        response = self.translation_client.translate_text(
            parent=self.parent,
            contents=[text],
            mime_type="text/plain",
            target_language_code=target_language_code
        )

        return {"translated_text": response.translations[0].translated_text}