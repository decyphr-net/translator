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
from .utils import LanguageProcessingMixin
from . import serializers


class FullTranslator(viewsets.ViewSet, LanguageProcessingMixin):
    """
    The translation endpoint that will be used to translate basic text into a
    target specified target language
    """

    serializer_class = serializers.BaseInputTranslation
    output_serializer = serializers.FullTranslatedSerializer

    def create(self, request):
        """
        The endpoint that will take the incoming data and language code and
        send it to Google to be translated. The response will come back from
        Google and it will be return the client.

        In addition to translating the text, this endpoint will also generate
        the audio file of the text and the analysis of the text according to
        Google's Natural Language service.

        Args:
            initial_language_code (str): A 4 character ISO 639-1 code to \
            identify the incoming language
            target_language_code (str): A ISO 639-1 code that will be used to \
            inform Google Translate of the target language
            text (str): The text that is needed to be translated
        
        Returns:
            JSON: The translated text and the location of the audio file, with
            the analysis of the text
        
        Example:
            curl -X POST -H "Content-type: application/json" \
                http://127.0.0.1:8000/api/v1/full-translation/ \
                -d '{"initial_language_code": "pt-BR", \
                     "target_language_code": "en", "text": "oi"}'
        """
        serializer = self.serializer_class(data=request.data)

        # If the incoming information is valid, then we'll translate the text
        # and return that newly created translation
        if serializer.is_valid():
            output = self.bundle_full_translation_response(serializer)
            return Response(output)
        else:
            return Response(serializer.errors)


class TextToTextTranslation(viewsets.ViewSet, LanguageProcessingMixin):
    """Text to text translation

    This view will be used to perform simple text to text translations that
    have no requirement to include
    """

    serializer_class = serializers.BaseInputTranslation
    output_serializer = serializers.TextToTextTranslatedSerializer

    def create(self, request):
        """
        The endpoint that will take the incoming data and language code and
        send it to Google to be translated. 

        This endpoint will only be used for straightforward text to text
        translations

        Args:
            target_language_code (str): A ISO 639-1 code that will be used \
            to inform Google Translate of the target language
            text (str): The text that is needed to be translated
        
        Returns:
            JSON: The translated text
        
        Example:
            curl -X POST -H "Content-type: application/json" \
                http://127.0.0.1:8000/api/v1/text-to-text/ \
                -d '{"target_language_code": "en", "text": "oi"}'
        """
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            if serializer.is_valid():
                output = self.bundle_text_translation_response(serializer)
                return Response(output)
            else:
                return Response(serializer.errors)
        else:
            return Response(serializer.errors)
