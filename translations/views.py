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
from .serializers import PlainTextTranslationSerializer


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
            language_code (str): A ISO 639-1 code that will be used to inform \
            Google Translate of the target language
            text (str): The text that is needed to be translated
        
        Returns:
            JSON:
                language_code (str): A ISO 639-1 code of the target language
                text (str): The text that is needed to be translated
                translated_text (str): The translated text
        
        Example:
            curl -X POST -H 'Content-type: application/json' \
                http://127.0.0.1:8000/api/v1/plain-text/ \
                -d '{"language_code": "en", "text": "oi"}'
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