"""
The views for the `translations`app.

This will be the only interface that consumers of this service will
communicate with.

The purpose of this will be to act as a bridge between the decyphr application
and the Google Translate API. Incoming text will be deserialized, translated
and returned back the cosumer that will ultimately be returned to an end user.
"""
from django.conf import settings
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from google.cloud import translate
from .serializers import PlainTextTranslationSerializer


class GoogleMixin:

    translation_client = translate.TranslationServiceClient()
    parent = translation_client.location_path(
        settings.GOOGLE_PROJECT, "global")

    def translate_text(self, target_language_code, text):
        response = self.translation_client.translate_text(
            parent=self.parent,
            contents=[text],
            mime_type="text/plain",
            target_language_code=target_language_code
        )

        return response.translations[0].translated_text


class PlainTextTranslator(viewsets.ViewSet, GoogleMixin):
    """
    The translation endpoint that will be used to translate basic text into a
    target specified target language
    """

    serializer_class = PlainTextTranslationSerializer

    def create(self, request):
        """
        The endpoint that will take the incoming data and language code and
        send it to Google to be translated. The response will come back from
        Google and it will be return the client

        Args:
            language_code (str): A ISO 639-1 code that will be used to inform
            Google Translate of the target language
            text (str): The text that is needed to be translated
        
        Returns:
            JSON:
                language_code (str): A ISO 639-1 code that will be used to
                inform Google Translate of the target language
                text (str): The text that is needed to be translated
                translated_text (str): The text that has been translated into
                the targetted language
        """
        language_code = request.data["language_code"]
        text = request.data["text"]

        translated_text = self.translate_text(language_code, text)
        
        data = {
            "language_code": language_code,
            "text": text,
            "translated_text": translated_text
        }
        
        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            return Response(serializer.data)
        else:
            return Response(serializer.errors)