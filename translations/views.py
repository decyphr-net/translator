"""
The views for the translations app.

This will be the only interface that consumers of this service will
communicate with.

The purpose of this will be to act as a bridge between the decyphr application
and the Google Translate API. Incoming text will be deserialized, translated
and returned back the cosumer that will ultimately be returned to an end user.
"""
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from .google_wrapper import GoogleMixin
from .serializers import (
    PlainTextTranslationSerializer, TranslatedTextSerializer)


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
            initial_language_code (str): A 4 character ISO 639-1 code to \
            identify the incoming language
            target_language_code (str): A ISO 639-1 code that will be used to \
            inform Google Translate of the target language
            text (str): The text that is needed to be translated
        
        Returns:
            JSON: The translated text and the location of the audio file
        
        Example:
            curl -X POST -H "Content-type: application/json" \
                http://127.0.0.1:8000/api/v1/plain-text/ \
                -d '{"initial_language_code": "pt-BR", \
                     "target_language_code": "en", "text": "oi"}'
        """
        serializer = self.serializer_class(data=request.data)

        # If the incoming information is valid, then we'll translate the text
        # and return that newly created translation
        if serializer.is_valid():
            translated_text = self.translate_text(
                serializer.data["target_language_code"],
                serializer.data["text"])
            audio_location = self.text_to_speech(
                serializer.data["text"],
                serializer.data["initial_language_code"])
            
            translated_data = {
                "translated_text": translated_text,
                "audio_location": audio_location
            }

            translated_text_serializer = TranslatedTextSerializer(
                data=translated_data)
            
            if translated_text_serializer.is_valid():
                return Response(translated_text_serializer.data)
            else:
                return Response(translated_text_serializer.errors)
        else:
            return Response(serializer.errors)